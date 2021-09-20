from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render, redirect
from service.utility.DataValidator import DataValidator
from service.service.UserService import UserService


class IndexCtl(BaseCtl):

    def request_to_form(self, requestFrom):
        self.form["loginId"] = requestFrom["loginId"]
        self.form["password"] = requestFrom["password"]

    def display(self, request, params={}):
        res = render(request, self.get_template())
        return res

    # Template html of Role page
    def get_template(self):
        return "ors/Index.html"

        # Service of Role
