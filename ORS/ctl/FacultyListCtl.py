from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.models import Faculty
from service.forms import FacultyForm
from service.service.FacultyService import FacultyService
from service.service.CourseService import CourseService
from service.service.SubjectService import SubjectService
from service.service.CollegeService import CollegeService


class FacultyListCtl(BaseCtl):
    count = 1

    # Populate Form from HTTP Request
    def request_to_form(self, requestForm):

        self.form["firstName"] = requestForm.get("firstName", None)
        self.form["lastName"] = requestForm.get("lastName", None)
        self.form["email"] = requestForm.get("email", None)
        self.form["password"] = requestForm.get("password", None)
        self.form["address"] = requestForm.get("address", None)
        self.form["gender"] = requestForm.get("gender", None)
        self.form["dob"] = requestForm.get("dob", None)
        self.form["college_ID"] = requestForm.get("college_ID", None)
        self.form["subject_ID"] = requestForm.get("subject_ID", None)
        self.form["subjectName"] = requestForm.get("subjectName", None)
        self.form["course_ID"] = requestForm.get("course_ID", None)
        self.form["courseName"] = requestForm.get("courseName", None)
        self.form["ids"] = requestForm.getlist("ids", None)

        # Display College page

    def display(self, request, params={}):
        record = self.get_service().search(self.form)
        self.page_list=record["data"]
        courseList = CourseService().preload(self.form)
        subject_List = SubjectService().preload(self.form)
        college_List = CollegeService().preload(self.form)
        for x in self.page_list:
            for y in courseList:
                if x.get("course_ID") == y.id:
                    x['courseName'] = y.courseName
            for z in subject_List:
                if x.get('subject_ID') == z.id:
                    x['subjectName'] = z.subjectName
            for c in college_List:
                if x.get('college_ID') == c.id:
                    x['collegeName'] = c.collegeName
        res = render(request, self.get_template(), {"pageList": self.page_list, "form": self.form})
        return res

    def next(self, request, params={}):
        FacultyListCtl.count += 1
        self.form["pageNo"] = FacultyListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        courseList = CourseService().preload(self.form)
        subject_List = SubjectService().preload(self.form)
        college_List = CollegeService().preload(self.form)
        for x in self.page_list:
            for y in courseList:
                if x.get("course_ID") == y.id:
                    x['courseName'] = y.courseName
            for z in subject_List:
                if x.get('subject_ID') == z.id:
                    x['subjectName'] = z.subjectName
            for c in college_List:
                if x.get('college_ID') == c.id:
                    x['collegeName'] = c.collegeName
        res = render(request, self.get_template(), {"pageList": self.page_list, "form": self.form})
        return res

    def previous(self, request, params={}):
        FacultyListCtl.count -= 1
        self.form["pageNo"] = FacultyListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        courseList = CourseService().preload(self.form)
        subject_List = SubjectService().preload(self.form)
        college_List = CollegeService().preload(self.form)
        for x in self.page_list:
            for y in courseList:
                if x.get("course_ID") == y.id:
                    x['courseName'] = y.courseName
            for z in subject_List:
                if x.get('subject_ID') == z.id:
                    x['subjectName'] = z.subjectName
            for c in college_List:
                if x.get('college_ID') == c.id:
                    x['collegeName'] = c.collegeName
        res = render(request, self.get_template(), {"pageList": self.page_list, "form": self.form})
        return res

    def submit(self, request, params={}):
        self.request_to_form(request.POST)
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        courseList = CourseService().preload(self.form)
        subject_List = SubjectService().preload(self.form)
        college_List = CollegeService().preload(self.form)
        for x in self.page_list:
            for y in courseList:
                if x.get("course_ID") == y.id:
                    x['courseName'] = y.courseName
            for z in subject_List:
                if x.get('subject_ID') == z.id:
                    x['subjectName'] = z.subjectName
            for c in college_List:
                if x.get('college_ID') == c.id:
                    x['collegeName'] = c.collegeName
        res = render(request, self.get_template(), {"pageList": self.page_list, "form": self.form})
        return res
    # Template html of Role page    
    def get_template(self):
        return "ors/FacultyList.html"

        # Service of Role

    def get_service(self):
        return FacultyService()

    def deleteRecord(self,request,params={}):
        FacultyListCtl.count+=1
        self.form["pageNo"]=1
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        courseList = CourseService().preload(self.form)
        subject_List = SubjectService().preload(self.form)
        college_List = CollegeService().preload(self.form)

        if(bool(self.form["ids"])==False):
            self.form["error"] = True
            self.form["message"] = "Please Select at least one check box"
            for x in self.page_list:
                for y in courseList:
                    if x.get("course_ID") == y.id:
                        x['courseName'] = y.courseName
                for z in subject_List:
                    if x.get('subject_ID') == z.id:
                        x['subjectName'] = z.subjectName
                for c in college_List:
                    if x.get('college_ID') == c.id:
                        x['collegeName'] = c.collegeName
            return render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
        else:
            for ids in self.form["ids"]:
                record = self.get_service().search(self.form)
                self.page_list=record["data"]
                id=int(ids)
                if( id > 0):
                    r = self.get_service().get(id)
                    if r is not None:
                        self.get_service().delete(r.id)
                        record = self.get_service().search(self.form)
                        self.page_list=record["data"]
                        self.form["pageNo"] = 1

                        self.form["error"] = False
                        self.form["message"] = "Data is successfully deleted"
                        for x in self.page_list:
                            for y in courseList:
                                if x.get("course_ID") == y.id:
                                    x['courseName'] = y.courseName
                            for z in subject_List:
                                if x.get('subject_ID') == z.id:
                                    x['subjectName'] = z.subjectName
                            for c in college_List:
                                if x.get('college_ID') == c.id:
                                    x['collegeName'] = c.collegeName
                        return render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
                    else:
                        self.form["error"] = True
                        self.form["message"] = "Data is not deleted"
                        for x in self.page_list:
                            for y in courseList:
                                if x.get("course_ID") == y.id:
                                    x['courseName'] = y.courseName
                            for z in subject_List:
                                if x.get('subject_ID') == z.id:
                                    x['subjectName'] = z.subjectName
                            for c in college_List:
                                if x.get('college_ID') == c.id:
                                    x['collegeName'] = c.collegeName
                        return render(request,self.get_template(),{"pageList":self.page_list,"form":self.form})
