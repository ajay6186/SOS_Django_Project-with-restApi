from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render


class WelcomeCtl(BaseCtl):

    def display(self, request, params={}):

        user = request.session.get("user", None)
        request.session["name"] = user.role_Name
        request.session["firstName"] = user.firstName
        request.session["lastName"] = user.lastName
        request.session["login_id"] = user.login_id

        if user:
            self.form["message"] = "Welcome to" + " " + user.role_Name
        return render(request, self.get_template(), {"form": self.form})

    def submit(self, request, params={}):
        return render(request, self.get_template(), {"form": self.form})

    # Template html of Role page    
    def get_template(self):
        return "ors/Welcome.html"

    # Service of Role
    def get_service(self):
        return "RoleService()"
