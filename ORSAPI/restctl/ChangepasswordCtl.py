from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render,redirect
from service.utility.DataValidator import DataValidator
from django.http.response import JsonResponse
from service.service.UserService import UserService
from service.service.EmailService import EmailService
from service.service.EmailMessage import EmailMessage
from service.models import User
import json


class ChangepasswordCtl(BaseCtl):
    def request_to_form(self,requestForm):
        self.form["id"]  = requestForm.get("id")
        # requestForm.get("login_id",None)
        self.form["newPassword"] = requestForm.get("newPassword",None)
        self.form["oldPassword"] = requestForm.get("oldPassword",None)
        self.form["confirmPassword"] = requestForm.get("confirmPassword",None)
        self.form['login_id'] = requestForm.get("login_id", None)
    #Populate Form from Model
    def model_to_form(self,obj):
        if (obj == None):
            return
        self.form["id"]  = obj.id
        self.form["newPassword"] = obj.newPassword
        self.form["oldPassword"] = obj.oldPassword
        self.form["confirmPassword"] = obj.confirmPassword

    #Convert form into module
    def form_to_model(self,obj):
        pk = int(self.form["id"])
        if(pk>0):
            obj.id = pk
        obj.newPassword=self.form["newPassword"]
        obj.oldPassword=self.form["oldPassword"]
        obj.confirmPassword=self.form["confirmPassword"]
        return obj

    def save(self,request,params={}):
        json_request =json.loads(request.body)
        self.request_to_form(json_request)
        if (self.input_validation()):
            self.form["error"] = True
            self.form["message"] = ""
            res =  JsonResponse({"form":self.form})
        else:
            user = User.objects.filter(login_id=self.form['login_id'])
            user = user[0]
            query = User.objects.filter(password=self.form["oldPassword"])
            if query.count()>0:
                if self.form["confirmPassword"]==self.form["newPassword"]:
                    emgs=EmailMessage()
                    emgs.to=[user.login_id]
                    emgs.subject="Change Password"
                    mailResponse=EmailService.send(emgs,"changePassword",user)
                    if(mailResponse==1):
                        convertUser=self.convert(user,user.id,self.form["newPassword"])
                        UserService().save(convertUser)
                        self.form["error"] = False
                        self.form["message"] = "Your password is change successfully, Please check your mail"
                        res = JsonResponse({"form":self.form})
                    else:
                        self.form["error"] = True
                        self.form["message"] = "Please check your Internet"
                        res = JsonResponse({"form":self.form})
                else:
                    self.form["error"] = True
                    self.form["confirmPassword"] = "Confirm password are not match"
                    res = JsonResponse({"form":self.form})
            else:
                self.form["error"] = True
                self.form["oldPassword"] = "oldPassword is wrong"
                res = JsonResponse({"form":self.form})
        return res

    def convert(self,u,uid,upass):
        u.id=uid
        u.password=upass
        return u

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
