


from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORSAPI.utility.DataValidator import DataValidator
from service.models import TimeTable
from service.forms import TimeTableForm
from service.service.TimeTableService import TimeTableService
from service.service.CourseService import CourseService
from service.service.SubjectService import SubjectService
from django.http.response import JsonResponse 
import json
# from django.core import serializers

class TimeTableCtl(BaseCtl): 
    
    def preload(self,request,params={}):
        
        courseList=CourseService().preload(self.form)
        subjectList = SubjectService().preload(self.form)
        coursedata=[]
        for x in courseList:
            coursedata.append(x.to_json())
        subpreload=[]
        for y in subjectList:
            subpreload.append(y.to_json())  
        return JsonResponse({"subpreload":subpreload,"coursedata":coursedata})

    def get(self,request, params = {}):
        service=TimeTableService()
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
        service=TimeTableService()
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
        courseList = CourseService().preload(self.form)
        subject_List = SubjectService().preload(self.form)
        if(json_request):
            params["subjectName"]=json_request.get("subjectName",None)
            params["semester"]=json_request.get("semester",None)
            params["pageNo"]=json_request.get("pageNo",None)
        service=TimeTableService()        
        c=service.search(params)
        res={}
        if(c!=None):
            for x in c['data']:
                for y in courseList:
                    if x.get("course_ID") == y.id:
                        x['courseName'] = y.courseName
                for z in subject_List:
                    if x.get("subject_ID") == z.id:
                        x['subjectName'] = z.subjectName
            res["data"]=c["data"]
            res["error"]=False
            res["message"]="Data is found"
        else:
            res["error"]=True
            res["message"]="record not found"
        return JsonResponse({"result":res})
        # print("tt search is found------------->")
        # json_request=json.loads(request.body)
        # if(json_request):
        #     params["subjectName"]=json_request.get("subjectName",None)
        #     params["semester"]=json_request.get("semester",None)    
        # service=TimeTableService()
        # c=service.search(params)
        # print(params," 1aaaaaaaaaaaaaaaa11111111111-->",c)

        # res={}
        # data=[]
        # courseList=CourseService().search(self.form)
        # subject_List = SubjectService().search(self.form)
        # for x in c: 
        #     for y in courseList:  
        #         if x.course_ID==y.id:
        #             x.courseName=y.courseName 
        #     for z in subject_List:               
        #        if x.subject_ID==z.id:
        #            x.subjectName=z.subjectName
        #     print("mk")       
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
        pk = int(request["id"])
        if(pk>0):
            obj.id = pk
        obj.examTime = request["examTime"]
        obj.examDate = request["examDate"]
        obj.subject_ID = request["subject_ID"] 
        obj.subjectName=request["subjectName"]
        obj.course_ID=request["course_ID"]
        obj.courseName=request["courseName"]
        obj.semester=request["semester"]
        return obj
  
    def save(self,request, params = {}):        
        json_request=json.loads(request.body)     
        r=self.form_to_model(TimeTable(), json_request)
        service=TimeTableService()
        c=service.save(r)
        res={}
        if(r!=None):
            res["data"]=r.to_json()
            res["error"]=False
            res["message"]="Data is Successfully saved"
        else:
            res["error"]=True
            res["message"]="Data is not saved"
        return JsonResponse({"data":res})

    # Template html of Role page    
    def get_template(self):
        return "orsapi/TimeTable.html"  

    def input_validation(self):
        super().input_validation()
        inputError =  self.form["inputError"]
        if(DataValidator.isNull(self.form["examTime"])):
            inputError["examTime"] = " examTime can not be null"
            self.form["error"] = True

        if(DataValidator.isNull(self.form["examDate"])):
            inputError["examDate"] = "examDate can not be null"
            self.form["error"] = True

        if(DataValidator.isNull(self.form["subject_ID"])):
            inputError["subject_ID"] = "subject_ID can not be null"
            self.form["error"] = True

        

    #     if(DataValidator.isNull(self.form["course_ID"])):
    #         inputError["course_ID"] = "course Name can not be null"
    #         self.form["error"] = True

       
    #     if(DataValidator.isNull(self.form["semester"])):
    #         inputError["semester"] = "semester can not be null"
    #         self.form["error"] = True

    #     return self.form["error"]         

    # Service of Role     
    def get_service(self):
        return TimeTableService()        


       



