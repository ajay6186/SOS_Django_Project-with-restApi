from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.forms import StudentForm
from service.models import Student
from service.service.StudentService import StudentService
from service.service.CollegeService import CollegeService


class StudentListCtl(BaseCtl):
    count = 1

    def request_to_form(self, requestForm):
        self.form["firstName"] = requestForm.get("firstName", None)
        self.form["lastName"] = requestForm.get("lastName", None)
        self.form["dob"] = requestForm.get("dob", None)
        self.form["mobileNumber"] = requestForm.get("mobileNumber", None)
        self.form["email"] = requestForm.get("email", None)
        self.form["college_ID"] = requestForm.get("college_ID", None)
        self.form["collegeName"] = requestForm.get("collegeName", None)
        self.form["ids"] = requestForm.getlist("ids", None)

    def display(self, request, params={}):
        record = self.get_service().search(self.form)
        self.page_list = record['data']
        collegeList = CollegeService().preload(self.form)
        for x in self.page_list:
            for y in collegeList:
                if x.get("college_ID") == y.id:
                     x["collegeName"] = y.collegeName
        res = render(request, self.get_template(), {"form": self.form, "pageList": self.page_list})
        return res

    def next(self, request, params={}):
        StudentListCtl.count += 1
        self.form["pageNo"] = StudentListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        collegeList = CollegeService().preload(self.form)
        for x in self.page_list:
            for y in collegeList:
                if x.get("college_ID") == y.id:
                    x["collegeName"] = y.collegeName
        res = render(request, self.get_template(), {"pageList": self.page_list, "form": self.form})
        return res

    def previous(self, request, params={}):
        StudentListCtl.count -= 1
        self.form["pageNo"] = StudentListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        collegeList = CollegeService().preload(self.form)
        for x in self.page_list:
            for y in collegeList:
                if x.get("college_ID") == y.id:
                    x["collegeName"] = y.collegeName
        res = render(request, self.get_template(), {"pageList": self.page_list, "form": self.form})
        return res

    def submit(self, request, params={}):
        self.request_to_form(request.POST)
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        collegeList = CollegeService().preload(self.form)
        for x in self.page_list:
            for y in collegeList:
                if x.get("college_ID") == y.id:
                    x["collegeName"] = y.collegeName
        res = render(request, self.get_template(), {"pageList": self.page_list, "form": self.form})
        return res

    def get_template(self):
        return "ors/StudentList.html"

        # Service of Marksheet

    def get_service(self):
        return StudentService()

    def deleteRecord(self, request, params={}):
        StudentListCtl.count += 1
        self.form["pageNo"] = 1
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        if (bool(self.form["ids"]) == False):
            self.form["error"] = True
            self.form["message"] = "Please Select at least one check box"
            collegeList = CollegeService().preload(self.form)
            for x in self.page_list:
                for y in collegeList:
                    if x.get("college_ID") == y.id:
                        x["collegeName"] = y.collegeName
            return render(request, self.get_template(), {"pageList": self.page_list, "form": self.form})
        else:
            for ids in self.form["ids"]:

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
                        collegeList = CollegeService().preload(self.form)
                        for x in self.page_list:
                            for y in collegeList:
                                if x.get("college_ID") == y.id:
                                    x["collegeName"] = y.collegeName
                        return render(request, self.get_template(), {"pageList": self.page_list, "form": self.form})
                    else:
                        self.form["error"] = True
                        self.form["message"] = "Data is not deleted"
                        collegeList = CollegeService().preload(self.form)
                        for x in self.page_list:
                            for y in collegeList:
                                if x.get("college_ID") == y.id:
                                    x["collegeName"] = y.collegeName
                        return render(request, self.get_template(), {"pageList": self.page_list, "form": self.form})
