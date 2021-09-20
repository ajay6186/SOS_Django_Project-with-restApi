from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORSAPI.utility.DataValidator import DataValidator
from service.models import Student
from service.forms import StudentForm
from service.service.StudentService import StudentService
from service.service.CollegeService import CollegeService 
from django.http.response import JsonResponse
import json


class StudentCtl(BaseCtl): 
    def preload(self,request,params={}):
        self.data = CollegeService().preload(self.form)
        preloadList=[]
        for x in self.data:
            preloadList.append(x.to_json())
            preloadList
        return JsonResponse({"preloadList":preloadList})
        
    def get(self,request, params = {}):
        
        service=StudentService()
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
        print("orsapi student delete is run")
        service=StudentService()
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
            params["collegeName"]=json_request.get("collegeName",None)
            params["pageNo"]=json_request.get("pageNo",None)
        service=StudentService()        
        c=service.search(params)
        res={}
        if(c!=None):
            collegeList = CollegeService().preload(self.form)
            for x in c['data']:
                for y in collegeList:
                    if x.get("college_ID") == y.id:
                        x["collegeName"] = y.collegeName
            res["data"]=c["data"]
            res["error"]=False
            res["message"]="Data is found"
        else:
            res["error"]=True
            res["message"]="record not found"
        return JsonResponse({"result":res})
       

    def form_to_model(self,obj,request):
        print("orsapi student form to model is run")
        c = CollegeService().get(self.form["college_ID"])       
        pk = int(request["id"])
        if(pk>0):
            obj.id = pk
        obj.firstName = request["firstName"]
        obj.lastName = request["lastName"]
        obj.dob=request["dob"] 
        obj.mobileNumber=request["mobileNumber"]
        obj.email=request["email"]
        obj.college_ID=request["college_ID"]
        obj.collegeName=c.collegeName
       
        return obj
 

    def save(self,request, params = {}):
            print("orsapi student save is run")      
            json_request=json.loads(request.body)
            self.request_to_form(json_request)
            res={}
            if(self.input_validation()):
                res["error"]=True 
                res["message"]=""
            else:
                r=self.form_to_model(Student(), json_request)
                service=StudentService()
                c=service.save(r)
                
                if(r!=None):
                    res["data"]=r.to_json()
                    res["error"]=False
                    res["message"]="Data is Successfully saved"    
            return JsonResponse({"data":res,'form':self.form})

    def request_to_form(self,requestForm):
       
        print("orsapi student request to form is run")
        self.form["id"]  = requestForm["id"]
        self.form["firstName"] = requestForm["firstName"]
        self.form["lastName"] = requestForm["lastName"]
        self.form["dob"] = requestForm["dob"]
        self.form["mobileNumber"] = requestForm["mobileNumber"]
        self.form["email"] = requestForm["email"]
        self.form["college_ID"] = requestForm["college_ID"]        
        # self.form["collegeName"] = requestForm["collegeName"]        

    def input_validation(self):
        super().input_validation()
        inputError =  self.form["inputError"]
        if(DataValidator.isNull(self.form["firstName"])):
            inputError["firstName"] = " First_Name can not be null"
            self.form["error"] = True

        if(DataValidator.isNull(self.form["lastName"])):
            inputError["lastName"] = "Last_Name can not be null"
            self.form["error"] = True

        if(DataValidator.isNull(self.form["dob"])):
            inputError["dob"] = "dob can not be null"
            self.form["error"] = True 

        if(DataValidator.isNull(self.form["mobileNumber"])):
            inputError["mobileNumber"] = "Mobile_Number can not be null"
            self.form["error"] = True

        if(DataValidator.isNull(self.form["email"])):
            inputError["email"] = "email_id can not be null"
            self.form["error"] = True

        if(DataValidator.isNull(self.form["college_ID"])):
            inputError["college_ID"] = "college_ID can not be null"
            self.form["error"] = True

        
        return self.form["error"]             

    # Template html of Role page    
    def get_template(self):
        return "orsapi/Student.html"          

    # Service of Role     
    def get_service(self):
        return StudentService()        
