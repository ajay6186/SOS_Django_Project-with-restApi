from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.models import Faculty
from service.forms import FacultyForm
from service.service.FacultyService import FacultyService
from service.service.SubjectService import SubjectService
from service.service.CollegeService import CollegeService
from service.service.CourseService import CourseService
from datetime import datetime
from django.utils.dateparse import parse_date


class FacultyCtl(BaseCtl):
    def preload(self, request):
        self.form['course_List'] = CourseService().preload(self.form)
        self.form['college_List'] = CollegeService().preload(self.form)
        self.form['subject_List'] = SubjectService().preload(self.form)

    # Populate Form from HTTP Request
    def request_to_form(self, requestForm):

        self.form["id"] = requestForm["id"]
        self.form["firstName"] = requestForm["firstName"]
        self.form["lastName"] = requestForm["lastName"]
        self.form["email"] = requestForm["email"]
        self.form["password"] = requestForm["password"]
        self.form["address"] = requestForm["address"]
        self.form["gender"] = requestForm["gender"]
        self.form["dob"] = requestForm["dob"]
        self.form["college_ID"] = requestForm["college_ID"]
        self.form["subject_ID"] = requestForm["subject_ID"]
        self.form["course_ID"] = requestForm["course_ID"]

    # Populate Form from Model
    def model_to_form(self, obj):

        if (obj == None):
            return
        self.form["id"] = obj.id
        self.form["firstName"] = obj.firstName
        self.form["lastName"] = obj.lastName
        self.form["email"] = obj.email
        self.form["password"] = obj.password

        self.form["address"] = obj.address
        self.form["gender"] = obj.gender
        self.form["dob"] = obj.dob
        self.form["college_ID"] = obj.college_ID
        self.form["subject_ID"] = obj.subject_ID
        # self.form["subjectName"] = obj.subjectName
        self.form["course_ID"] = obj.course_ID

    # Convert form into module
    def form_to_model(self, obj):
        c = CourseService().get(self.form["course_ID"])
        e = CollegeService().get(self.form["college_ID"])
        s = SubjectService().get(self.form["subject_ID"])
        pk = int(self.form["id"])
        if (pk > 0):
            obj.id = pk
        obj.firstName = self.form["firstName"]
        obj.lastName = self.form["lastName"]
        obj.email = self.form["email"]
        obj.password = self.form["password"]

        obj.address = self.form["address"]
        obj.gender = self.form["gender"]
        obj.dob = self.form["dob"]
        obj.college_ID = self.form["college_ID"]
        obj.subject_ID = self.form["subject_ID"]

        obj.course_ID = self.form["course_ID"]

        obj.courseName = c.courseName
        obj.collegeName = e.collegeName
        obj.subjectName = s.subjectName
        return obj

    # Validate form
    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["firstName"])):
            inputError["firstName"] = " First Name can not be null"
            self.form["error"] = True
        else:
            if DataValidator.isaplhacheck(self.form["firstName"]):
                inputError["firstName"] = "Name contains only alphabets"
                self.form["error"] = True

        if (DataValidator.isNull(self.form["lastName"])):
            inputError["lastName"] = "Last Name can not be null"
            self.form["error"] = True
        else:
            if DataValidator.isaplhacheck(self.form["lastName"]):
                inputError["lastName"] = "Name contains only alphabets"
                self.form["error"] = True

        if (DataValidator.isNull(self.form["email"])):
            inputError["email"] = "Email ID can not be null"
            self.form["error"] = True
        else:
            if (DataValidator.isemail(self.form['email'])):
                inputError['email'] = "Please Enter Email Address"
                self.form['error'] = True

        if (DataValidator.isNull(self.form["password"])):
            inputError["password"] = "Password can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["address"])):
            inputError["address"] = "Address can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["gender"])):
            inputError["gender"] = "Gender can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["dob"])):
            inputError["dob"] = "DOB can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["college_ID"])):
            inputError["college_ID"] = "College Name can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["subject_ID"])):
            inputError["subject_ID"] = "Subject Name can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["course_ID"])):
            inputError["course_ID"] = "Course ID Name not be null"
            self.form["error"] = True

        return self.form["error"]

    def display(self, request, params={}):
        if (params["id"] > 0):
            r = self.get_service().get(params["id"])
            self.model_to_form(r)
        res = render(request, self.get_template(),
                     {"form": self.form})
        return res

    def submit(self, request, params={}):
        if params['id'] > 0:
            pk = params['id']
            dup = self.get_service().get_model().objects.exclude(id=pk).filter(email=self.form["email"])
            if dup.count() > 0:
                self.form["error"] = True
                self.form['message'] = "Email id already exists"
                res = render(request, self.get_template(), {"form": self.form})
            else:
                r = self.form_to_model(Faculty())
                self.get_service().save(r)
                self.form["id"] = r.id
                self.form["error"] = False
                self.form["message"] = "Data is updated successfully"
                res = render(request, self.get_template(), {"form": self.form})
            return res
        else:
            duplicate = self.get_service().get_model().objects.filter(email=self.form["email"])
            if duplicate.count() > 0:
                self.form["error"] = True
                self.form["message"] = "Email id is already exists"
                res = render(request, self.get_template(),
                             {"form": self.form})
            else:
                r = self.form_to_model(Faculty())
                self.get_service().save(r)
                self.form["id"] = r.id
                self.form["error"] = False
                self.form["message"] = "Data is successfully saved"
                res = render(request, self.get_template(), {"form": self.form})
        return res

    # Template html of Role page
    def get_template(self):
        return "ors/Faculty.html"

    # Service of Role

    def get_service(self):
        return FacultyService()
