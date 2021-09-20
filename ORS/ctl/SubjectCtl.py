from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render, redirect
from ORS.utility.DataValidator import DataValidator
from service.models import Subject
from service.forms import SubjectForm
from service.service.SubjectService import SubjectService
from service.service.CollegeService import CollegeService
from service.service.CourseService import CourseService


class SubjectCtl(BaseCtl):

    def preload(self, request):
        self.form['Course_List'] = CourseService().preload(self.form)

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form["subjectName"] = requestForm["subjectName"]
        self.form["subjectDescription"] = requestForm["subjectDescription"]
        self.form["course_ID"] = requestForm["course_ID"]

    # Populate Form from Model
    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form["id"] = obj.id
        self.form["subjectName"] = obj.subjectName
        self.form["subjectDescription"] = obj.subjectDescription

        self.form["course_ID"] = obj.course_ID

    # Convert form into module
    def form_to_model(self, obj):
        c = CourseService().get(self.form["course_ID"])
        pk = int(self.form["id"])
        if (pk > 0):
            obj.id = pk
        obj.subjectName = self.form["subjectName"]
        obj.subjectDescription = self.form["subjectDescription"]
        obj.course_ID = self.form["course_ID"]
        obj.courseName = c.courseName
        return obj

    # Validate form
    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["subjectName"])):
            inputError["subjectName"] = " subjectName can not be null"
            self.form["error"] = True
        else:
            if DataValidator.isaplhacheck(self.form["subjectName"]):
                inputError["subjectName"] = "Name contains only alphabets"
                self.form["error"] = True

        if (DataValidator.isNull(self.form["subjectDescription"])):
            inputError["subjectDescription"] = "subjectDescription can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["course_ID"])):
            inputError["course_ID"] = "course ID can not be null"
            self.form["error"] = True

        return self.form["error"]

        # Display Marksheet page

    def display(self, request, params={}):
        if (params["id"] > 0):
            r = self.get_service().get(params["id"])
            self.model_to_form(r)
        res = render(request, self.get_template(), {"form": self.form})
        return res

    # Submit Marksheet page
    def submit(self, request, params={}):
        if params['id'] > 0:
            pk = params['id']
            dup = self.get_service().get_model().objects.exclude(id=pk).filter(subjectName=self.form["subjectName"])
            if dup.count() > 0:
                self.form["error"] = True
                self.form['message'] = "Subject Name already exists"
                res = render(request, self.get_template(), {"form": self.form})
            else:
                r = self.form_to_model(Subject())
                self.get_service().save(r)
                self.form["id"] = r.id
                self.form["error"] = False
                self.form["message"] = "Data is Updated successfully"
                res = render(request, self.get_template(), {"form": self.form})
            return res
        else:
            duplicate = self.get_service().get_model().objects.filter(subjectName=self.form["subjectName"])
            if duplicate.count() > 0:
                self.form["error"] = True
                self.form["message"] = "Subject is already exists"
                res = render(request, self.get_template(),
                             {"form": self.form})
            else:
                r = self.form_to_model(Subject())
                self.get_service().save(r)
                self.form["id"] = r.id
                self.form["error"] = False
                self.form["message"] = "Data is successfully saved"
                res = render(request, self.get_template(), {"form": self.form})
            return res

    # Template html of Student page    
    def get_template(self):
        return "ORS/Subject.html"

        # Service of Student

    def get_service(self):
        return SubjectService()
