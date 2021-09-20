from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.models import Marksheet
from service.forms import MarksheetForm
from service.service.MarksheetService import MarksheetService
from service.service.StudentService import StudentService


class MarksheetCtl(BaseCtl):
    def preload(self, request):
        self.page_list = StudentService().search(self.form)
        self.preloadData = self.page_list

    # Populate Form from HTTP Request
    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form["rollNumber"] = requestForm["rollNumber"]
        self.form["name"] = requestForm["name"]
        self.form["physics"] = requestForm["physics"]
        self.form["chemistry"] = requestForm["chemistry"]
        self.form["maths"] = requestForm["maths"]

    # Populate Form from Model
    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form["id"] = obj.id
        self.form["rollNumber"] = obj.rollNumber
        self.form["name"] = obj.name
        self.form["physics"] = obj.physics
        self.form["chemistry"] = obj.chemistry
        self.form["maths"] = obj.maths

    # Convert form into module
    def form_to_model(self, obj):

        pk = int(self.form["id"])
        if (pk > 0):
            obj.id = pk
        obj.rollNumber = self.form["rollNumber"]
        obj.name = self.form["name"]
        obj.physics = self.form["physics"]
        obj.chemistry = self.form["chemistry"]
        obj.maths = self.form["maths"]

        return obj

    # Validate form
    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["rollNumber"])):
            inputError["rollNumber"] = "Roll Number can not be null"
            self.form["error"] = True
        else:
            if (DataValidator.ischeckroll(self.form['rollNumber'])):
                inputError['rollNumber'] = "Roll No. contain Alpha Numeric e.g SOS123"
                self.form['error'] = True

        if (DataValidator.isNull(self.form["name"])):
            inputError["name"] = "Name can not be null"
            self.form["error"] = True
        else:
            if DataValidator.isaplhacheck(self.form["name"]):
                inputError["name"] = "Name contains only alphabets"
                self.form["error"] = True

        if (DataValidator.isNull(self.form["physics"])):
            inputError["physics"] = "Physics marks can not be null"
            self.form["error"] = True
        else:
            if (DataValidator.ischeck(self.form['physics'])):
                inputError['physics'] = "Physics marks in between 0 to 100"
                self.form['error'] = True

        if (DataValidator.isNull(self.form["chemistry"])):
            inputError["chemistry"] = "Chemistry marks can not be null"
            self.form["error"] = True
        else:
            if (DataValidator.ischeck(self.form['chemistry'])):
                inputError['chemistry'] = "Chemistry marks in between 0 to 100"
                self.form['error'] = True

        if (DataValidator.isNull(self.form["maths"])):
            inputError["maths"] = "Maths marks can not be null"
            self.form["error"] = True
        else:
            if (DataValidator.ischeck(self.form['maths'])):
                inputError['maths'] = "Maths marks in between 0 to 100"
                self.form['error'] = True

        return self.form["error"]

        # Display Marksheet page

    def display(self, request, params={}):
        if (params["id"] > 0):
            r = self.get_service().get(params["id"])
            self.model_to_form(r)
        res = render(request, self.get_template(), {"form": self.form, "studentList": self.preloadData})
        return res

    # Submit Marksheet page
    def submit(self, request, params={}):
        if params['id'] > 0:
            pk = params['id']
            dup = self.get_service().get_model().objects.exclude(id=pk).filter(rollNumber=self.form["rollNumber"])
            if dup.count() > 0:
                self.form["error"] = True
                self.form['message'] = " Roll Number already exists"
                res = render(request, self.get_template(), {"form": self.form})
            else:
                r = self.form_to_model(Marksheet())
                self.get_service().save(r)
                self.form["id"] = r.id
                self.form["error"] = False
                self.form["message"] = "Data is update successfully"
                res = render(request, self.get_template(), {"form": self.form})
            return res
        else:
            duplicate = self.get_service().get_model().objects.filter(rollNumber=self.form["rollNumber"])
            if duplicate.count() > 0:
                self.form["error"] = True
                self.form["message"] = "Roll Number is already exists"
                res = render(request, self.get_template(),
                             {"form": self.form})
            else:
                r = self.form_to_model(Marksheet())
                self.get_service().save(r)
                self.form["id"] = r.id
                self.form["error"] = False
                self.form["message"] = "Data is successfully saved"
                res = render(request, self.get_template(), {"form": self.form})
            return res

    # Template html of Marksheet page
    def get_template(self):
        return "ors/Marksheet.html"

    # Service of Marksheet
    def get_service(self):
        return MarksheetService()
