



from django.http import HttpResponse

from service.service.CollegeService import CollegeService
from service.service.CourseService import CourseService
from service.service.SubjectService import SubjectService
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORSAPI.utility.DataValidator import DataValidator
from service.models import Faculty
from service.forms import FacultyForm
from service.service.FacultyService import FacultyService
from django.http.response import JsonResponse
import json
from django.core import serializers   

class FacultyCtl(BaseCtl): 
    def preload(self,request,params={}):
        print("tt preload is run")

        courseList=CourseService().preload(self.form)
        subjectList = SubjectService().preload(self.form)
        collegeList = CollegeService().preload(self.form)
        coursedata=[]
        subpreload = []
        collegeload = []
        for x in courseList:
            coursedata.append(x.to_json())
        for y in subjectList:
            subpreload.append(y.to_json())
        for z in collegeList:
            collegeload.append(z.to_json())
        return JsonResponse({"subpreload": subpreload,"coursedata": coursedata, "collegeload": collegeload})
<<<<<<< HEAD
    
=======

>>>>>>> 4dda84088e1d455acca1459810c682ff83a41715
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

        

    def get(self,request, params = {}):
        service=FacultyService()
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
        service=FacultyService()
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
        return JsonResponse({"data":res})


    def search(self,request, params = {}):
        print("faculty search is found")
        json_request=json.loads(request.body)
        courseList = CourseService().preload(self.form)
        subject_List = SubjectService().preload(self.form)
        college_List = CollegeService().preload(self.form)
        if(json_request):
<<<<<<< HEAD
            params["collegeName"]=json_request.get("collegeName",None)
=======
            params["email"]=json_request.get("email",None)
>>>>>>> 4dda84088e1d455acca1459810c682ff83a41715
            params["pageNo"]=json_request.get("pageNo",None)
        service=FacultyService()
        c=service.search(params)
        res={}
        if(c!=None):
            for x in c['data']:
                for y in courseList:
                    if x.get("course_ID") == y.id:
                        x['courseName'] = y.courseName
                for z in subject_List:
                    if x.get('subject_ID') == z.id:
                        x['subjectName'] = z.subjectName
                for cl in college_List:
                    if x.get('college_ID') == cl.id:
                        x['collegeName'] = cl.collegeName
            res["data"] = c['data']
            res["error"]=False
            res["message"]="Data is found"
        else:
            res["error"]=True
            res["message"]="record not found"
        return JsonResponse({"data":res})

    def form_to_model(self,obj,request):
        pk = int(request["id"])
        if(pk>0):
            obj.id = pk
        obj.firstName = request["firstName"]
        obj.lastName = request["lastName"]
        obj.email=request["email"] 
        obj.password=request["password"] 
        obj.address=request["address"]  
        obj.gender=request["gender"]  
        obj.dob=request["dob"]  
        obj.college_ID=request["college_ID"]  
        obj.subject_ID=request["subject_ID"]  
        obj.course_ID=request["course_ID"]  
        # obj.collegeName=request["collegeName"]
               
        return obj

    def save(self,request, params = {}):      
        json_request=json.loads(request.body)
        self.request_to_form(json_request)
        res={}
        if(self.input_validation()):
            res["error"]=True
            res["message"]="Data is not saved"
        else:
            r=self.form_to_model(Faculty(), json_request)
            service=FacultyService()
            c=service.save(r)
            
            if(r!=None):
                res["data"]=r.to_json()
                res["error"]=False
                res["message"]="Data is Successfully saved"    
        return JsonResponse({"data":res,'form':self.form})

    def input_validation(self):
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["firstName"])):
            inputError["firstName"] = "Name can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["lastName"])):
            inputError["lastName"] = "last name can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["email"])):
            inputError["email"] = "email can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["password"])):
            inputError["password"] = "password can not be null"
            self.form["error"] = True
        
        if (DataValidator.isNull(self.form["address"])):
            inputError["address"] = "Address can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["gender"])):
            inputError["gender"] = "gender can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["dob"])):
            inputError["dob"] = "dob can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["college_ID"])):
            inputError["college_ID"] = "college_ID can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["subject_ID"])):
            inputError["subject_ID"] = "subject_ID can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["course_ID"])):
            inputError["course_ID"] = "course_ID can not be null"
            self.form["error"] = True                  
        return self.form["error"]

    # Template html of Role page    
    def get_template(self):
        return "orsapi/AddFaculty.html"          

    # Service of Role     
    def get_service(self):
        return FacultyService()        
