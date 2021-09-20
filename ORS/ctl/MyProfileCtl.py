from django.shortcuts import render, redirect
from service.utility.DataValidator import DataValidator
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from service.models import User
from service.service.UserService import UserService
from service.service.RoleService import RoleService
from django.contrib.sessions.models import Session


class MyProfileCtl(BaseCtl):
    def preload(self, request):
        self.page_list = RoleService().search(self.form)
        self.preloadData = self.page_list

    # Populate Form from HTTP Request
    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]

    # Populate Form from Model
    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form["id"] = obj.id
        self.form["firstName"] = obj.firstName
        self.form["lastName"] = obj.lastName
        self.form["login_id"] = obj.login_id
        self.form["password"] = obj.password
        self.form["dob"] = obj.dob
        self.form["mobilenumber"] = obj.mobilenumber
        self.form["gender"] = obj.gender

    # Convert form into module
    def form_to_model(self, obj):
        pk = int(self.form["id"])
        if (pk > 0):
            obj.id = pk
        obj.firstName = self.form["firstName"]
        obj.lastName = self.form["lastName"]
        obj.login_id = self.form["login_id"]
        obj.password = self.form["password"]
        obj.dob = self.form["dob"]
        obj.mobilenumber = self.form["mobilenumber"]
        obj.gender = self.form["gender"]

        return obj

    # Display Role page

    def display(self, request, params={}):

        user = request.session.get("user", None)
        if (user is not None):
            self.form["username"] = user.login_id
        if (user.id > 0):
            r = self.get_service().get(user.id)
            self.model_to_form(r)
        res = render(request, self.get_template(), {"form": self.form, "roleList": self.preloadData})
        return res

    # Submit Role page
    def submit(self, request, params={}):
        r = self.form_to_model(User())
        self.get_service().save(r)
        self.form["id"] = r.id
        self.form["error"] = False
        self.form["message"] = "Data is saved"
        res = render(request, self.get_template(), {"form": self.form})
        return res

    def deleteRecord(self, request, params={}):
        id = int(self.form['id'])
        if id > 0:
            r = self.get_service().get(self.form['id'])
            if r is not None:
                self.get_service().delete(r.id)
                Session.objects.all().delete()
                self.form["error"] = False
                self.form["message"] = "ID successfully deleted"
                return render(request, "ors/Login.html", {"form": self.form})
            else:
                self.form["error"] = True
                self.form["message"] = "Data is not delete"
                return HttpResponse(self.form['message'])
        return HttpResponse("Something Went Wrong")

    def get_template(self):
        return "ors/MyProfile.html"

        # Service of Role

    def get_service(self):
        return UserService()
