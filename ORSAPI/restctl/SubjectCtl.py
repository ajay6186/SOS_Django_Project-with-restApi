
 

from django.http import HttpResponse 
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORSAPI.utility.DataValidator import DataValidator
from service.models import Subject 
from service.forms import SubjectForm
from service.service.SubjectService import SubjectService
from service.service.CourseService import CourseService 
from django.http.response import JsonResponse
import json
from django.core import serializers

class SubjectCtl(BaseCtl): 
    def preload(self,request,params={}):
        self.data = CourseService().preload(self.form)
        preloadList=[]
        for x in self.data:
            preloadList.append(x.to_json())
        return JsonResponse({"preloadList":preloadList})

    def request_to_form(self,requestForm):
        self.form["id"]  = requestForm["id"]
        self.form["subjectName"] = requestForm["subjectName"]
        self.form["subjectDescription"] = requestForm["subjectDescription"]       
        self.form["course_ID"] = requestForm["course_ID"]
       
    def get(self,request, params = {}):
        service=SubjectService()
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
        service=SubjectService()
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
            params["subjectName"]=json_request.get("subjectName",None)
            params["pageNo"]=json_request.get("pageNo",None)
     
        service=SubjectService()        
        c=service.search(params)
       
        res={}
        if(c!=None):
            courseList = CourseService().preload(self.form)
            for x in c['data']:
                for y in courseList:
                    if x.get('course_ID') == y.id:
                        x['courseName'] = y.courseName

            res["data"]=c["data"]
            res["error"]=False
            res["message"]="Data is found"
        else:
            res["error"]=True
            res["message"]="record not found"
        return JsonResponse({"result":res})
        # json_request=json.loads(request.body)
        # if(json_request):
        #     params["subjectName"]=json_request.get("subjectName",None)
                        
        # service=SubjectService()
        # c=service.search(params)
        # res={}
        # data=[]
        # courseList=CourseService().search(self.form)
        # for x in c:
        #     for y in courseList:
        #         if x.course_ID==y.id:
        #             x.courseName=y.courseName
        #             print("ddddd----------->",x.courseName)
        #     data.append(x.to_json())
        # if(c!=None):
        #     res["data"]=data
        #     res["error"]=False
        #     res["message"]="Data is found"
        # else:
        #     res["error"]=True
        #     res["message"]="record not found"
        # return JsonResponse({"data":res})

    def form_to_model(self,obj,request):
        c = CourseService().get(self.form["course_ID"])
        pk = int(self.form["id"])
        if(pk>0):
            obj.id = pk
        obj.subjectName=self.form["subjectName"]
        obj.subjectDescription=self.form["subjectDescription"]       
        obj.course_ID=self.form["course_ID"]        
        obj.courseName=c.courseName
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
            r=self.form_to_model(Subject(),json_request)
            service=SubjectService()
            c=service.save(r)
            
            if(r!=None):
                res["data"]=r.to_json()
                res["error"]=False
                res["message"]="Data is Successfully saved"    
        return JsonResponse({"data":res,'form':self.form})
    
    def input_validation(self):
        # super().input_validation()
        inputError =  self.form["inputError"]
        if(DataValidator.isNull(self.form["subjectName"])):
            inputError["subjectName"] = " subjectName can not be null"
            self.form["error"] = True

        if(DataValidator.isNull(self.form["subjectDescription"])):
            inputError["subjectDescription"] = "subjectDescription can not be null"
            self.form["error"] = True

        if(DataValidator.isNull(self.form["course_ID"])):
            inputError["course_ID"] = "course_ID can not be null"
            self.form["error"] = True

        return self.form["error"]        


    # Template html of Role page    
    def get_template(self):
        return "orsapi/Subject.html"          

    # Service of Role     
    def get_service(self):
        return SubjectService()        


       



