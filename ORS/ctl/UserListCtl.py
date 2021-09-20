from django.shortcuts import render, redirect
from service.utility.DataValidator import DataValidator
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from service.models import User
from service.service.UserService import UserService
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class UserListCtl(BaseCtl):
    count = 1

    def request_to_form(self, requestForm):
        self.form["firstName"] = requestForm.get("firstName", None)
        self.form["lastName"] = requestForm.get("lastName", None)
        self.form["login_id"] = requestForm.get("login_id", None)
        self.form["ids"] = requestForm.getlist("ids", None)

    def display(self, request, params={}):
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        res = render(request, self.get_template(), {"pageList": self.page_list, "form": self.form})
        return res

    def next(self, request, params={}):
        UserListCtl.count += 1
        self.form["pageNo"] = UserListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record["data"]

        res = render(request, self.get_template(), {"pageList": self.page_list, "form": self.form})
        return res

    def previous(self, request, params={}):
        user = request.session.get('user', None)
        UserListCtl.count -= 1
        self.form["pageNo"] = UserListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record["data"]

        res = render(request, self.get_template(), {"pageList": self.page_list, "form": self.form})
        return res

    def deleteRecord(self, request, params={}):
        UserListCtl.count += 1
        self.form["pageNo"] = 1
        if (bool(self.form["ids"]) == False):
            self.form["error"] = True
            self.form["message"] = "Please Select at least one check box"
            record = self.get_service().search(self.form)
            self.page_list = record["data"]
            return render(request, self.get_template(), {"pageList": self.page_list, "form": self.form})
        else:
            for ids in self.form["ids"]:
                record = self.get_service().search(self.form)
                self.page_list = record["data"]
                id = int(ids)
                if (id > 0):
                    r = self.get_service().get(id)
                    if r is not None:
                        self.get_service().delete(r.id)
                        record = self.get_service().search(self.form)
                        self.page_list = record["data"]
                        self.form["pageNo"] = 1

                        self.form["error"] = False
                        self.form["message"] = "DATA IS SUCCESSFULLY DELETED"

                        return render(request, self.get_template(), {"pageList": self.page_list, "form": self.form})
                    else:
                        self.form["error"] = True
                        self.form["message"] = "Data is not deleted"
                        return render(request, self.get_template(), {"pageList": self.page_list, "form": self.form})

    def submit(self, request, params={}):
        self.request_to_form(request.POST)
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        res = render(request, self.get_template(), {"pageList": self.page_list, "form": self.form})
        return res

    def get_template(self):
        return "ors/UserList.html"
        # Service of Role

    def get_service(self):
        return UserService()
