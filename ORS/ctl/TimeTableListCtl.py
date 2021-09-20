from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.forms import TimeTableForm
from service.models import TimeTable
from service.service.TimeTableService import TimeTableService
from service.service.CourseService import CourseService
from service.service.SubjectService import SubjectService


class TimeTableListCtl(BaseCtl):
    count = 1
    def request_to_form(self, requestForm):
        self.form["examTime"] = requestForm.get("examTime", None)
        self.form["examDate"] = requestForm.get("examDate", None)
        self.form["subjectName"] = requestForm.get("subjectName", None)
        self.form["course_ID"] = requestForm.get("course_ID", None)
        self.form["semester"] = requestForm.get("semester", None)
        self.form["ids"] = requestForm.getlist("ids", None)


    def display(self, request, params={}):
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        courseList = CourseService().preload(self.form)
        subject_List = SubjectService().preload(self.form)
        for x in self.page_list:
            for y in courseList:
                if x.get("course_ID") == y.id:
                    x['courseName'] = y.courseName
            for z in subject_List:
                if x.get("subject_ID") == z.id:
                    x['subjectName'] = z.subjectName
        res = render(request, self.get_template(), {"pageList": self.page_list, "form": self.form})
        return res

    def next(self, request, params={}):
        TimeTableListCtl.count += 1
        self.form["pageNo"] = TimeTableListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        courseList = CourseService().preload(self.form)
        subject_List = SubjectService().preload(self.form)
        for x in self.page_list:
            for y in courseList:
                if x.get("course_ID") == y.id:
                    x['courseName'] = y.courseName
            for z in subject_List:
                if x.get("subject_ID") == z.id:
                    x['subjectName'] = z.subjectName
        res = render(request, self.get_template(), {"pageList": self.page_list, "form": self.form})
        return res

    def previous(self, request, params={}):
        TimeTableListCtl.count -= 1
        self.form["pageNo"] = TimeTableListCtl.count
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        courseList = CourseService().preload(self.form)
        subject_List = SubjectService().preload(self.form)
        for x in self.page_list:
            for y in courseList:
                if x.get("course_ID") == y.id:
                    x['courseName'] = y.courseName
            for z in subject_List:
                if x.get("subject_ID") == z.id:
                    x['subjectName'] = z.subjectName
        res = render(request, self.get_template(), {"pageList": self.page_list, "form": self.form})
        return res

    def submit(self, request, params={}):
        self.request_to_form(request.POST)
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        courseList = CourseService().preload(self.form)
        subject_List = SubjectService().preload(self.form)
        for x in self.page_list:
            for y in courseList:
                if x.get("course_ID") == y.id:
                    x['courseName'] = y.courseName
            for z in subject_List:
                if x.get("subject_ID") == z.id:
                    x['subjectName'] = z.subjectName
        res = render(request, self.get_template(), {"pageList": self.page_list, "form": self.form})
        return res

    def get_template(self):
        return "ors/TimeTableList.html"

        # Service of Marksheet

    def get_service(self):
        return TimeTableService()


    def deleteRecord(self, request, params={}):
        TimeTableListCtl.count += 1
        self.form["pageNo"] = 1
        record = self.get_service().search(self.form)
        self.page_list = record["data"]
        courseList = CourseService().preload(self.form)
        subject_List = SubjectService().preload(self.form)
        if (bool(self.form["ids"]) == False):
            self.form["error"] = True
            self.form["message"] = "Please Select at least one check box"
            for x in self.page_list:
                for y in courseList:
                    if x.get("course_ID") == y.id:
                        x['courseName'] = y.courseName
                for z in subject_List:
                    if x.get("subject_ID") == z.id:
                        x['subjectName'] = z.subjectName
            return render(request, self.get_template(), {"pageList": self.page_list, "form": self.form})
        else:
            for ids in self.form["ids"]:

                id = int(ids)
                if (id > 0):
                    r = self.get_service().get(id)
                    if r is not None:
                        self.get_service().delete(r.id)
                        record = self.get_service().search(self.form)
                        self.page_list = record["data"]
                        self.form["pageNo"] = 1
                        self.form["error"] = False
                        self.form["message"] = "DATA IS SUCCESSFULLY DELETED"
                        for x in self.page_list:
                            for y in courseList:
                                if x.get("course_ID") == y.id:
                                    x['courseName'] = y.courseName
                            for z in subject_List:
                                if x.get("subject_ID") == z.id:
                                    x['subjectName'] = z.subjectName
                        return render(request, self.get_template(), {"pageList": self.page_list, "form": self.form})
                    else:
                        self.form["error"] = True
                        self.form["message"] = "Data is not deleted"
                        for x in self.page_list:
                            for y in courseList:
                                if x.get("course_ID") == y.id:
                                    x['courseName'] = y.courseName
                            for z in subject_List:
                                if x.get("subject_ID") == z.id:
                                    x['subjectName'] = z.subjectName
                        return render(request, self.get_template(), {"pageList": self.page_list, "form": self.form})
