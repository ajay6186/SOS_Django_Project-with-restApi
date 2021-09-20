


from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORSAPI.utility.DataValidator import DataValidator
from service.models import Marksheet
from service.forms import MarksheetForm
from service.service.MarksheetService import MarksheetService
from django.http.response import JsonResponse
import json
from django.core import serializers

class MarksheetCtl(BaseCtl): 
    def request_to_form(self,requestForm):
        self.form["id"]  = requestForm["id"]
        self.form["rollNumber"] = requestForm["rollNumber"]
        self.form["name"] = requestForm["name"]
        self.form["physics"] = requestForm["physics"]
        self.form["chemistry"] = requestForm["chemistry"]
        self.form["maths"] = requestForm["maths"]
        # self.form["student_ID"] = requestForm["student_ID"]



    def get(self,request, params = {}):
        service=MarksheetService()
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
        service=MarksheetService()
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

    def search(self,request, params = {}):
        json_request=json.loads(request.body)
        if(json_request):
            params["name"]=json_request.get("name",None)
            params["rollNumber"]=json_request.get("rollNumber",None)
            params["pageNo"]=json_request.get("pageNo",None)
     
        service=MarksheetService()        
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
        obj.rollNumber = request["rollNumber"]
        obj.name = request["name"]
        obj.physics=request["physics"]
        obj.physics=request["physics"] 
        obj.chemistry=request["chemistry"] 
        obj.maths=request["maths"] 
        # obj.student_ID=request["student_ID"]
        return obj

    def save(self,request, params = {}):
            
        json_request=json.loads(request.body)
        self.request_to_form(json_request)
        res={}
        if(self.input_validation()):
            res["error"]=True
            res["message"]=""               
        else:
            r=self.form_to_model(Marksheet(), json_request)
            service=MarksheetService()
            c=service.save(r)
            
            if(r!=None):
                res["data"]=r.to_json()
                res["error"]=False
                res["message"]="Data is Successfully saved" 
                    
        return JsonResponse({"data":res,'form':self.form})

    def input_validation(self):
        super().input_validation()
        inputError =  self.form["inputError"]
        if(DataValidator.isNull(self.form["rollNumber"])):
            inputError["rollNumber"] = "roll Number can not be null"
            self.form["error"] = True

        if(DataValidator.isNull(self.form["name"])):
            inputError["name"] = "name can not be null"
            self.form["error"] = True

        if(DataValidator.ischeck(self.form["physics"])) :
            inputError["physics"] = "Enter marks 1 to 100"
            self.form["error"] = True     

        if(DataValidator.isNull(self.form["physics"])) :
            inputError["physics"] = "physics marks can not be null"
            self.form["error"] = True
          
        if(DataValidator.ischeck(self.form["chemistry"])):
            inputError["chemistry"] = "Enter marks 1 to 100" 
            self.form["error"] = True   


        if(DataValidator.isNull(self.form["chemistry"])):
            inputError["chemistry"] = "chemistry marks can not be null"
            self.form["error"] = True

        if(DataValidator.ischeck(self.form["maths"])):
            inputError["maths"] = "Enter marks 1 to 100" 
            self.form["error"] = True      
        
        if(DataValidator.isNull(self.form["maths"])):
            inputError["maths"] = "maths marks can not be null"
            self.form["error"] = True
        
        return self.form["error"]        
    

    # Template html of Role page    
    def get_template(self):
        return "orsapi/Marksheet.html"          

    # Service of Role     
    def get_service(self):
        return MarksheetService()        


       



