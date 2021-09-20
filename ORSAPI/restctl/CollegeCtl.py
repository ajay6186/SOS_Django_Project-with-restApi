from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORSAPI.utility.DataValidator import DataValidator
from service.models import College
from service.forms import CollegeForm
from service.service.CollegeService import CollegeService
from django.http.response import JsonResponse
import json


# from django.core import serializers

class CollegeCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form["collegeName"] = requestForm["collegeName"]
        self.form["collegeAddress"] = requestForm["collegeAddress"]
        self.form["collegeState"] = requestForm["collegeState"]
        self.form["collegeCity"] = requestForm["collegeCity"]
        self.form["collegePhoneNumber"] = requestForm["collegePhoneNumber"]

    def get(self, request, params={}):

        service = CollegeService()
        c = service.get(params["id"])
        res = {}
        if (c != None):
            res["data"] = c.to_json()
            res["error"] = False
            res["message"] = "Data is found"
        else:
            res["error"] = True
            res["message"] = "record not found"
        return JsonResponse({"data": res["data"]})

    def delete(self, request, params={}):
        service = CollegeService()
        c = service.get(params["id"])
        res = {}
        if (c != None):
            service.delete(params["id"])
            res["data"] = c.to_json()
            res["error"] = False
            res["message"] = "Data is Successfully deleted"
        else:
            res["error"] = True
            res["message"] = "Data is not deleted"
        return JsonResponse({"data": res})

    def search(self, request, params={}):
        json_request = json.loads(request.body)
        if (json_request):
            params["collegeName"] = json_request.get("collegeName", None)
            params["pageNo"] = json_request.get("pageNo", None)
        service = CollegeService()
        c = service.search(params)
        res = {}
        if (c != None):
            res["data"] = c["data"]
            res["error"] = False
            res["message"] = "Data is found"
        else:
            res["error"] = True
            res["message"] = "record not found"
        return JsonResponse({"data": res})

    def form_to_model(self, obj, request):
        print("orsapi college form to model is run")
        pk = int(request["id"])
        if (pk > 0):
            obj.id = pk
        obj.collegeName = request["collegeName"]
        obj.collegeAddress = request["collegeAddress"]
        obj.collegeState = request["collegeState"]
        obj.collegeCity = request["collegeCity"]
        obj.collegePhoneNumber = request["collegePhoneNumber"]
        return obj

    def save(self, request, params={}):
        json_request = json.loads(request.body)
        self.request_to_form(json_request)
        res = {}
        if (self.input_validation()):
            res["error"] = True
            res["message"] = ""
        else:
            r = self.form_to_model(College(), json_request)
            service = CollegeService()
            c = service.save(r)
            if (r != None):
                res["data"] = r.to_json()
                res["error"] = False
                res["message"] = "Data is Successfully saved"
        return JsonResponse({"data": res, 'form': self.form})

    def input_validation(self):
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["collegeName"])):
            inputError["collegeName"] = "Name can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["collegeAddress"])):
            inputError["collegeAddress"] = "Address can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["collegeState"])):
            inputError["collegeState"] = "State can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["collegeCity"])):
            inputError["collegeCity"] = "City can not be null"
            self.form["error"] = True
        if (DataValidator.isNull(self.form["collegePhoneNumber"])):
            inputError["collegePhoneNumber"] = "PhoneNumber can not be null"
            self.form["error"] = True
        return self.form["error"]

    # Template html of Role page
    def get_template(self):
        return "orsapi/College.html"

        # Service of Role

    def get_service(self):
        return CollegeService()






