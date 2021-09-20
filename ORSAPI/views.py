from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ORSAPI.restctl.CollegeCtl import CollegeCtl
from ORSAPI.restctl.CourseCtl import CourseCtl
from ORSAPI.restctl.RegistrationCtl import RegistrationCtl

from ORSAPI.restctl.UserCtl import UserCtl

from ORSAPI.restctl.RoleCtl import RoleCtl
from ORSAPI.restctl.MarksheetCtl import MarksheetCtl
from ORSAPI.restctl.StudentCtl import StudentCtl

from ORSAPI.restctl.SubjectCtl import SubjectCtl
from ORSAPI.restctl.ChangepasswordCtl import ChangepasswordCtl
from ORSAPI.restctl.TimeTableCtl import TimeTableCtl
from ORSAPI.restctl.ForgetpasswordCtl import ForgetpasswordCtl
from ORSAPI.restctl.FacultyCtl import FacultyCtl
# from ORSAPI.restctl.FacultyListCtl import FacultyListCtl

from ORSAPI.restctl.LoginCtl import LoginCtl

from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def info(request, page, action):
    print("REQ Method: ", request.method)
    print("Page: ", page)
    print("Action: ", action)
    print("Base Path: ", __file__)


@csrf_exempt
def action(request, page, action="get", id=0):
    info(request, page, action)

    methodCall = page + "Ctl()." + action + "(request,{'id':id})"
    response = eval(methodCall)
    return response
