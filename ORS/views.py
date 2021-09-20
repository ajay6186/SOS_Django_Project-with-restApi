from django.conf.urls.static import static
from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session

# import controller classes
from ORS.ctl.UserCtl import UserCtl
from ORS.ctl.CollegeCtl import CollegeCtl
from ORS.ctl.LoginCtl import LoginCtl
from ORS.ctl.WelcomeCtl import WelcomeCtl
from ORS.ctl.RoleCtl import RoleCtl
from ORS.ctl.RoleListCtl import RoleListCtl
from ORS.ctl.FacultyCtl import FacultyCtl
from ORS.ctl.FacultyListCtl import FacultyListCtl
from ORS.ctl.CourseCtl import CourseCtl
from ORS.ctl.StudentCtl import StudentCtl
from ORS.ctl.MarksheetCtl import MarksheetCtl

from ORS.ctl.SubjectCtl import SubjectCtl
from ORS.ctl.SubjectListCtl import SubjectListCtl
from ORS.ctl.TimeTableCtl import TimeTableCtl
from ORS.ctl.TimeTableListCtl import TimeTableListCtl
from ORS.ctl.UserListCtl import UserListCtl
from ORS.ctl.UserCtl import UserCtl
from ORS.ctl.CollegeListCtl import CollegeListCtl

from ORS.ctl.CourseListCtl import CourseListCtl
from ORS.ctl.MarksheetListCtl import MarksheetListCtl
from ORS.ctl.StudentListCtl import StudentListCtl
from ORS.ctl.RegistrationCtl import RegistrationCtl
from ORS.ctl.ForgetPasswordCtl import ForgetPasswordCtl
from ORS.ctl.ChangePasswordCtl import ChangePasswordCtl
from ORS.ctl.LogoutCtl import LogoutCtl
from ORS.ctl.IndexCtl import IndexCtl
from ORS.ctl.MyProfileCtl import MyProfileCtl
from ORS.ctl.HomeCtl import HomeCtl


def info(request, page, action):
    print("REQ Method: ", request.method)
    print("Page: ", page)
    print("Action: ", action)
    print("Base Path: ", __file__)


'''
Calls respective controller with id
'''


@csrf_exempt
def actionId(request, page="", operation="", id=0):
    info(request, page, id)
    if request.session.get('user') is not None and page != "":
        ctlName = page + "Ctl()"
        ctlObj = eval(ctlName)
        res = ctlObj.execute(request, {"id": id})
    elif page == "Registration":
        ctlName = "Registration" + "Ctl()"
        ctlObj = eval(ctlName)
        res = ctlObj.execute(request, {"id": id})
    elif (page == "Home"):
        ctlName = "Home" + "Ctl()"
        ctlObj = eval(ctlName)
        res = ctlObj.execute(request, {"id": id})

    elif (page == "ForgetPassword"):
        ctlName = "ForgetPassword" + "Ctl()"
        ctlObj = eval(ctlName)
        res = ctlObj.execute(request, {"id": id})

    elif (page == "Login"):
        ctlName = "Login" + "Ctl()"
        ctlObj = eval(ctlName)
        res = ctlObj.execute(request, {"id": id})

    else:
        res = redirect("/ORS/Login")
    return res


@csrf_exempt
def auth(request, page="", operation="", id=0):
    print("Auth-->", info(request, page, id))
    if page == "Logout":
        Session.objects.all().delete()
        ctlName = page + "Ctl()"
        ctlObj = eval(ctlName)
        res = ctlObj.execute(request, {"id": id, "operation": operation})

    elif page == "ForgetPassword":
        ctlName = "ForgetPassword" + "Ctl()"
        ctlObj = eval(ctlName)
        res = ctlObj.execute(request, {"id": id, "operation": operation})

    else:
        ctlName = "Login" + "Ctl()"
        ctlObj = eval(ctlName)
        res = ctlObj.execute(request, {"id": id, "operation": operation})
    return res


def index(request):
    res = render(request, 'ors/project.html')
    print("Index function running")
    return res
