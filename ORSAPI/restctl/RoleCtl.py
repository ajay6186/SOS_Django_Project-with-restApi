


from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORSAPI.utility.DataValidator import DataValidator
from service.models import Role
from service.forms import RoleForm
from service.service.RoleService import RoleService
from django.http.response import JsonResponse
import json
from django.core import serializers

class RoleCtl(BaseCtl):
    def request_to_form(self,requestForm):
        self.form["id"]  = requestForm["id"]
        self.form["name"] = requestForm["name"]
        self.form["description"] = requestForm["description"]
 
    def get(self,request, params = {}):
        service=RoleService()
        c=service.get(params["id"])
        res={}
        if(c!=None):
            res["data"]=c.to_json()
            res["error"]=False
            res["message"]="Data is found"
        else:
            res["error"]=True
            res["message"]="record not found"
        return JsonResponse({"data":res["data"]})

    def delete(self,request, params = {}):
        service=RoleService()
        c=service.get(params["id"])
        res={}
        if(c!=None):
            service.delete(params["id"])
            res["data"]=c.to_json()
            res["error"]=False
            res["message"]="Data is Successfully deleted"
        else:
            res["error"]=True
            res["message"]="Data is not deleted"
        return JsonResponse({"data":res["data"]})

    # def search(self,request, params = {}):
    #     json_request=json.loads(request.body)
    #     if(json_request):
    #         params["name"]=json_request.get("name",None)
            
    #     service=RoleService()
    #     c=service.search(params)
    #     res={}
    #     data=[]
    #     for x in c:
    #         data.append(x.to_json())
    #     if(c!=None):
    #         res["data"]=data
    #         res["error"]=False
    #         res["message"]="Data is found"
    #     else:
    #         res["error"]=True
    #         res["message"]="record not found"
    #     return JsonResponse({"data":res})
    def search(self,request, params = {}):
        json_request=json.loads(request.body)
        if(json_request):
            params["name"]=json_request.get("name",None)
            params["pageNo"]=json_request.get("pageNo",None)
     
        service=RoleService()        
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

        
    def form_to_model(self,obj,request):
        pk = int(request["id"])
        if(pk>0):
            obj.id = pk
        obj.name = request["name"]
        obj.description = request["description"]
        
        return obj

    def save(self,request, params = {}):
        print("orsapi college save is run")      
        json_request=json.loads(request.body)
        self.request_to_form(json_request)
        res={}
        if(self.input_validation()):
            res["error"]=True
            res["message"]=""
        else:
            r=self.form_to_model(Role(), json_request)
            service=RoleService()
            c=service.save(r)
            
            if(r!=None):
                res["data"]=r.to_json()
                res["error"]=False
                res["message"]="Data is Successfully saved"    
        return JsonResponse({"data":res,'form':self.form})
    
    def input_validation(self):
        # super().input_validation()
        inputError =  self.form["inputError"]
        if(DataValidator.isNull(self.form["name"])):
            inputError["name"] = "Name can not be null"
            self.form["error"] = True
        if(DataValidator.isNull(self.form["description"])):
            inputError["description"] = "Description can not be null"
            self.form["error"] = True
        return self.form["error"]        


    # Template html of Role page    
    def get_template(self):
        return "orsapi/Role.html"          

    # Service of Role     
    def get_service(self):
        return RoleService()        


       



