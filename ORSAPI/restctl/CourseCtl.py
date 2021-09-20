from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORSAPI.utility.DataValidator import DataValidator
from service.models import Course
from service.forms import CourseForm
from service.service.CourseService import CourseService
from django.http.response import JsonResponse
import json
from django.core import serializers


class CourseCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm["id"]
        self.form["courseName"] = requestForm["courseName"]
        self.form["courseDescription"] = requestForm["courseDescription"]
        self.form["courseDuration"] = requestForm["courseDuration"]
        # self.form["id"]= requestForm.get( "id", None)

    def get(self, request, params={}):
        service = CourseService()
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
        service = CourseService()
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
        return JsonResponse({"data": res["data"]})

<<<<<<< HEAD
    

    def search(self,request, params = {}):
        json_request=json.loads(request.body)
        if(json_request):
            params["courseName"]=json_request.get("courseName",None)
            params["pageNo"]=json_request.get("pageNo",None)
     
        service=CourseService()        
        c=service.search(params)
       
        res={}
        if(c!=None):
            res["data"]=c["data"]
            res["error"]=False
            res["message"]="Data is found"
        else:
            res["error"]=True
            res["message"]="record not found"
        return JsonResponse({"result":res})
       
=======
    def search(self, request, params={}):
        json_request = json.loads(request.body)
        if (json_request):
            params["courseName"] = json_request.get("courseName", None)
            params["pageNo"] = json_request.get("pageNo", None)
        service = CourseService()
        c = service.search(params)

        res = {}
        if (c != None):
            res["data"] = c["data"]
            res["error"] = False
            res["message"] = "Data is found"
        else:
            res["error"] = True
            res["message"] = "record not found"
        return JsonResponse({"result": res})
>>>>>>> 4dda84088e1d455acca1459810c682ff83a41715

    def form_to_model(self, obj, request):
        pk = int(request["id"])
        if (pk > 0):
            obj.id = pk
        obj.courseName = request["courseName"]
        obj.courseDescription = request["courseDescription"]
        obj.courseDuration = request["courseDuration"]
        return obj

    def save(self, request, params={}):
        # print("orsapi college save is run")      
        json_request = json.loads(request.body)
        self.request_to_form(json_request)
        res = {}
        if (self.input_validation()):
            res["error"] = True
            res["message"] = ""

        else:
            r = self.form_to_model(Course(), json_request)
            service = CourseService()
            c = service.save(r)
            if (r != None):
                res["data"] = r.to_json()
                res["error"] = False
                res["message"] = "Data is Successfully saved"
        return JsonResponse({"data": res, 'form': self.form})

    def input_validation(self):
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["courseName"])):
            inputError["courseName"] = "courseName can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["courseDescription"])):
            inputError["courseDescription"] = "courseDescription can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["courseDuration"])):
            inputError["courseDuration"] = "courseDuration can not be null"
            self.form["error"] = True

        return self.form["error"]

    # Template html of Role page
    def get_template(self):
        return "orsapi/Course.html"

        # Service of Role

    def get_service(self):
        return CourseService()
