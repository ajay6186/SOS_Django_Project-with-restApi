from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.models import User
from service.service.ChangePasswordService import ChangePasswordService
from service.service.EmailMessage import EmailMessage
from service.service.EmailService import EmailService
from service.service.UserService import UserService


class ChangePasswordCtl(BaseCtl):
    # Populate Form from HTTP Request
    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form["newPassword"] = requestForm["newPassword"]
        self.form["oldPassword"] = requestForm["oldPassword"]
        self.form["confirmPassword"] = requestForm["confirmPassword"]

    # Populate Form from Model
    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form["id"] = obj.id
        self.form["newPassword"] = obj.newPassword
        self.form["oldPassword"] = obj.oldPassword
        self.form["confirmPassword"] = obj.confirmPassword

    # Convert form into module
    def form_to_model(self, obj):
        pk = int(self.form["id"])
        if (pk > 0):
            obj.id = pk
        obj.newPassword = self.form["newPassword"]
        obj.oldPassword = self.form["oldPassword"]
        obj.confirmPassword = self.form["confirmPassword"]
        return obj

    # Validate form
    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["newPassword"])):
            inputError["newPassword"] = "New Password can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["oldPassword"])):
            inputError["oldPassword"] = "Old Password can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["confirmPassword"])):
            inputError["confirmPassword"] = "Confirm Password can not be null"
            self.form["error"] = True
        return self.form["error"]

        # Display Change Password page

    def display(self, request, params={}):
        if (params["id"] > 0):
            r = self.get_service().get(params["id"])
            self.model_to_form(r)
        res = render(request, self.get_template(), {"form": self.form})
        return res

    # Submit Change Password page
    def submit(self, request, params={}):
        user = request.session.get("user", None)
        q = User.objects.filter(password=self.form["oldPassword"])
        if q.count() > 0:
            if self.form["confirmPassword"] == self.form["newPassword"]:
                emgs = EmailMessage()
                emgs.to = [user.login_id]
                emgs.subject = "Change Password"
                mailResponse = EmailService.send(emgs, "changePassword", user)
                if (mailResponse == 1):
                    convertUser = self.convert(user, user.id, self.form["newPassword"])
                    UserService().save(convertUser)
                    self.form["error"] = False
                    self.form["message"] = "Your password is change successfully, Please check your mail"
                    res = render(request, self.get_template(), {"form": self.form})
                else:
                    self.form["error"] = True
                    self.form["message"] = "Please check your Internet Connection "
                    res = render(request, self.get_template(), {"form": self.form})
            else:
                self.form["error"] = True
                self.form["confirmPassword"] = "Confirm password are not match"
                res = render(request, self.get_template(), {"form": self.form})
        else:
            self.form["error"] = True
            self.form["oldPassword"] = "OldPassword is wrong"
            res = render(request, self.get_template(), {"form": self.form})
        return res

    def convert(self, u, uid, upass):
        u.id = uid
        u.password = upass
        return u

    # Template html of Change Password page
    def get_template(self):
        return "ors/ChangePassword.html"

        # Service of Role

    def get_service(self):
        return ChangePasswordService()
