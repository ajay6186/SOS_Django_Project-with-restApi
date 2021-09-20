from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render, redirect
from service.utility.DataValidator import DataValidator
from service.service.UserService import UserService


class LogoutCtl(BaseCtl):

    def display(self, request, params={}):
        request.session["user"] = None
        self.form["message"] = "Logout Successful"
        res = render(request, self.get_template(), {"form": self.form})

        return res

    def submit(self, request, params={}):
        pass

    # Template html of Role page    
    def get_template(self):
        return "ors/Login.html"

        # Service of Role

    def get_service(self):
        return UserService()
