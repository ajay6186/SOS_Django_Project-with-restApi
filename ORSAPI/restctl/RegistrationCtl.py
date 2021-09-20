from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORSAPI.utility.DataValidator import DataValidator
from service.models import User
from service.forms import UserForm
from service.service.UserService import UserService
from service.service.EmailService import EmailService
from service.service.EmailMessage import EmailMessage

from django.http.response import JsonResponse
import json


class RegistrationCtl(BaseCtl):
    def get(self, request, params={}):
        service = UserService()
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
        service = UserService()
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

    def search(self, request, params={}):
        json_request = json.loads(request.body)
        if (json_request):
            params["login_id"] = json_request.get("login_id", None)
            params["pageNo"] = json_request.get("pageNo", None)
        service = UserService()
        c = service.search(params)
        res = {}
        data = []
        for x in c:
            data.append(x)
        if (c != None):
            res["data"] = data
            res["error"] = False
            res["message"] = "Data is found"
        else:
            res["error"] = True
            res["message"] = "record not found"
        return JsonResponse({"data": res})

    def request_to_form(self, requestForm):

        self.form["id"] = requestForm["id"]
        self.form["firstName"] = requestForm["firstName"]
        self.form["lastName"] = requestForm["lastName"]
        self.form["login_id"] = requestForm["login_id"]
        self.form["password"] = requestForm["password"]
        self.form["confirmpassword"] = requestForm["confirmpassword"]
        self.form["dob"] = requestForm["dob"]
        self.form["address"] = requestForm["address"]

        self.form["gender"] = requestForm["gender"]
        self.form["mobilenumber"] = requestForm["mobilenumber"]
        self.form["role_Id"] = 2
        # self.form["role_Name"] = "Student"

    # Populate Form from Model
    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form["id"] = obj.id
        self.form["firstName"] = obj.firstName
        self.form["lastName"] = obj.lastName
        self.form["login_id"] = obj.login_id
        self.form["password"] = obj.password
        self.form["confirmpassword"] = obj.confirmpassword
        self.form["dob"] = obj.dob
        self.form["address"] = obj.address
        self.form["gender"] = obj.gender
        self.form["mobilenumber"] = obj.mobilenumber
        self.form["role_Id"] = 2
        # self.form["role_Name"] = "Student"

    # Convert form into module
    def form_to_model(self, obj, request):
        pk = int(request["id"])
        if (pk > 0):
            obj.id = pk
        obj.firstName = request["firstName"]
        obj.lastName = request["lastName"]
        obj.login_id = request["login_id"]
        obj.password = request["password"]
        obj.confirmpassword = request["confirmpassword"]
        obj.dob = request["dob"]
        obj.address = request["address"]
        obj.gender = request["gender"]
        obj.mobilenumber = request["mobilenumber"]
        obj.role_Id = request["role_Id"]
        # obj.role_Name = request["role_Name"]
        return obj

    # Validate form
    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["firstName"])):
            inputError["firstName"] = "Name can not be null"
            self.form["error"] = True
        if (DataValidator.isNull(self.form["lastName"])):
            inputError["lastName"] = "Last Name can not be null"
            self.form["error"] = True
        if (DataValidator.isNull(self.form["login_id"])):
            inputError["login_id"] = "Login can not be null"
            self.form["error"] = True
        if (DataValidator.isNull(self.form["password"])):
            inputError["password"] = "Password can not be null"
            self.form["error"] = True
        if (DataValidator.isNull(self.form["confirmpassword"])):
            inputError["confirmpassword"] = "confirmpassword can not be null"
            self.form["error"] = True
        if (DataValidator.isNotNull(self.form["confirmpassword"])):
            if (self.form["password"] != self.form["confirmpassword"]):
                inputError["conpassword"] = "Password and confirm Password are not Same"
                self.form["error"] = True

        if (DataValidator.isNull(self.form["dob"])):
            inputError["dob"] = "dob can not be null"
            self.form["error"] = True
        if (DataValidator.isNull(self.form["address"])):
            inputError["address"] = "address can not be null"
            self.form["error"] = True
        if (DataValidator.isNull(self.form["mobilenumber"])):
            inputError["mobilenumber"] = "mobileNumber can not be null"
            self.form["error"] = True
<<<<<<< HEAD
        return self.form["error"]        

    def save(self,request, params = {}):
        json_request=json.loads(request.body)

        self.request_to_form(json_request) 
        res={}
        if(self.input_validation()):
            res["error"]=True
            res["message"]=""
           
        else:
            emsg=EmailMessage()
            emsg.to= [self.form["login_id"]]
            e={}
            e["login"]= self.form["login_id"]
            e["password"]=self.form["password"]
            emsg.subject= "ORS Registration Successful"    
      
            mailResponse=EmailService.send(emsg,"signUp",e)  
            r=self.form_to_model(User(), json_request)
            service=UserService()
            c=service.save(r)
            res={}
       
            if(mailResponse==1):
                res["data"]=r.to_json()
                res["error"]=False
                res["message"]="Data is Successfully saved"
            else:
                res["error"]=True
                res["message"]="Data is not saved"
        return JsonResponse({"form":self.form,"data":res})
    
 
         
=======
        return self.form["error"]

    def save(self, request, params={}):
        json_request = json.loads(request.body)

        self.request_to_form(json_request)
        res = {}
        if (self.input_validation()):
            res["error"] = True
            res["message"] = ""

        else:
            emsg = EmailMessage()
            emsg.to = [self.form["login_id"]]
            e = {}
            e["login"] = self.form["login_id"]
            e["password"] = self.form["password"]
            emsg.subject = "ORS Registration Successful"

            mailResponse = EmailService.send(emsg, "signUp", e)
            r = self.form_to_model(User(), json_request)
            service = UserService()
            c = service.save(r)
            res = {}

            if (mailResponse == 1):
                res["data"] = r.to_json()
                res["error"] = False
                res["message"] = "Data is Successfully saved"
            else:
                res["error"] = True
                res["message"] = "Data is not saved"
        return JsonResponse({"form": self.form, "data": res})
>>>>>>> 4dda84088e1d455acca1459810c682ff83a41715
