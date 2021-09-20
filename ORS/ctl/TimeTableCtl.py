from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORS.utility.DataValidator import DataValidator
from service.models import TimeTable
from service.forms import TimeTableForm
from service.service.TimeTableService import TimeTableService
from service.service.CollegeService import CollegeService
from service.service.CourseService import CourseService
from service.service.SubjectService import SubjectService
from datetime import datetime
from django.utils.dateparse import parse_date


class TimeTableCtl(BaseCtl):
    def preload(self, request):
        self.form['course_List'] = CourseService().preload(self.form)
        self.form['subject_List'] = SubjectService().preload(self.form)

        # Populate Form from HTTP Request

    def request_to_form(self, requestForm):

        self.form["id"] = requestForm["id"]
        self.form["examTime"] = requestForm["examTime"]
        self.form["examDate"] = requestForm["examDate"]
        self.form["subject_ID"] = requestForm["subject_ID"]
        self.form["course_ID"] = requestForm["course_ID"]
        self.form["semester"] = requestForm["semester"]

    # Populate Form from Model
    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form["id"] = obj.id
        self.form["examTime"] = obj.examTime
        self.form["examDate"] = obj.examDate
        self.form["subject_ID"] = obj.subject_ID
        self.form["course_ID"] = obj.course_ID
        self.form["semester"] = obj.semester

    # Convert form into module
    def form_to_model(self, obj):
        c = CourseService().get(self.form["course_ID"])
        s = SubjectService().get(self.form["subject_ID"])
        pk = int(self.form["id"])
        newdate = ""
        if (pk > 0):
            obj.id = pk
        obj.examTime = self.form["examTime"]
        obj.examDate = self.form["examDate"]
        obj.subject_ID = self.form["subject_ID"]
        obj.course_ID = self.form["course_ID"]
        obj.semester = self.form["semester"]
        obj.courseName = c.courseName
        obj.subjectName = s.subjectName
        return obj

    # Validate form
    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["examTime"])):
            inputError["examTime"] = "Exam Time can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["examDate"])):
            inputError["examDate"] = "Exam Date can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["subject_ID"])):
            inputError["subject_ID"] = "Subject_ID can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["course_ID"])):
            inputError["course_ID"] = "Course Name can not be null"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["semester"])):
            inputError["semester"] = "Semester can not be null"
            self.form["error"] = True

        return self.form["error"]

    # Display Marksheet page

    def display(self, request, params={}):
        if (params["id"] > 0):
            r = self.get_service().get(params["id"])
            self.model_to_form(r)
        res = render(request, self.get_template(),
                     {"form": self.form})
        return res

    # Submit Marksheet page
    def submit(self, request, params={}):
        if params['id'] > 0:
            dup = self.get_service().get_model().objects.exclude(id=params['id']).filter(
                course_ID=self.form["course_ID"], subject_ID=self.form["subject_ID"], examDate=self.form["examDate"], examTime= self.form['examTime'], semester = self.form["semester"])
            if dup.count() > 0:
                self.form["error"] = True
                self.form['message'] = "Data already exists"
                res = render(request, self.get_template(), {"form": self.form})
            else:
                r = self.form_to_model(TimeTable())
                self.get_service().save(r)
                self.form["id"] = r.id
                self.form["error"] = False
                self.form["message"] = "Data is successfully Updated"
                res = render(request, self.get_template(),
                             {"form": self.form})

        else:
            duplicity = self.get_service().Duplicate(self.form["course_ID"], self.form["subject_ID"],
                                                     self.form["examDate"], self.form['examTime'], self.form["semester"])
            if duplicity.count() > 0:
                self.form["error"] = True
                self.form["message"] = "Data is already exists"
                res = render(request, self.get_template(),
                             {"form": self.form})

            else:

                r = self.form_to_model(TimeTable())
                self.get_service().save(r)
                self.form["id"] = r.id
                self.form["error"] = False
                self.form["message"] = "Data is successfully saved"
                res = render(request, self.get_template(),
                             {"form": self.form})
        return res

    # Template html of Student page

    def get_template(self):
        return "ors/TimeTable.html"

    # Service of Student

    def get_service(self):
        return TimeTableService()
