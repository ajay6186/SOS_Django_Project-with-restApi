from django.http import HttpResponse
from .BaseCtl import BaseCtl
from django.shortcuts import render
from ORSAPI.utility.DataValidator import DataValidator
from service.models import User
from service.forms import UserForm
from service.service.UserService import UserService
from django.http.response import JsonResponse
from service.service.EmailService import EmailService
from service.service.EmailMessage import EmailMessage
from service.service.EmailBuilder import EmailBuilder
import json
from django.contrib.sessions.models import Session


class LoginCtl(BaseCtl):
    def request_to_form(self, requestForm):
        self.form["login_id"] = requestForm.get("login_id", None)
        self.form["password"] = requestForm.get("password", None)

    def form_to_model(self, obj, request):
        obj.login_id = request["login_id"]
        obj.password = request["password"]
        return obj

    def logout(self, request, params={}):
        Session.objects.all().delete()
        self.form["error"] = False
        self.form["message"] = "Logout successfully"
        res = JsonResponse({"form": self.form})
        return res

<<<<<<< HEAD
    def auth(self,request,params = {}):
        json_request=json.loads(request.body)  
        self.request_to_form(json_request)
         
        q = User.objects.filter()
        res={}
        

        if(self.input_validation()):
            res["error"]=True
            res["message"]=""
            
            
        else:
            if(json_request.get("login_id")!=None ):
                q= q.filter( login_id = json_request.get("login_id"))  
            if(json_request.get("password")!=None ):
                q= q.filter( password = json_request.get("password"))
                userList = q
        #
            if (userList.count() > 0): 
                self.form["error"]=False
                self.form["message"]="Login Successfully"
                request.session["user"] = userList[0]        
                data= userList[0].to_json()
                self.form["sessionKey"]=request.session.session_key
                self.form["data"]=data
                # res=JsonResponse({"form":self.form,"data":res})
            else:
                self.form["error"]=True
                self.form["message"]="Login Id and Password is wrong"
                # res=JsonResponse({"form":self.form,"data":res})
        return JsonResponse({"form":self.form,"data":res})
=======
    def auth(self, request, params={}):
        json_request = json.loads(request.body)
        self.request_to_form(json_request)
        q = User.objects.filter()
        res = {}
        if (self.input_validation()):
            res["error"] = True
            res["message"] = ""
        else:
            if (json_request.get("login_id") != None):
                q = q.filter(login_id=json_request.get("login_id"))
            if (json_request.get("password") != None):
                q = q.filter(password=json_request.get("password"))
                userList = q
            if (userList.count() > 0):
                self.form["error"] = False
                self.form["message"] = "Login Successfully"
                request.session["user"] = userList[0]
                data = userList[0].to_json()
                self.form["sessionKey"] = request.session.session_key
                self.form["data"] = data
                # res=JsonResponse({"form":self.form,"data":res})
            else:
                self.form["error"] = True
                self.form["message"] = "Login Id and Password is wrong"
                # res=JsonResponse({"form":self.form,"data":res})
        return JsonResponse({"form": self.form, "data": res})
>>>>>>> 4dda84088e1d455acca1459810c682ff83a41715

    def Forgetpassword(self, request, params={}):
        json_request = json.loads(request.body)
        self.request_to_form(json_request)
        q = User.objects.filter(login_id=self.form["login_id"])
        userList = q[0]
        if (userList != ""):
            emsg = EmailMessage()
            emsg.to = [userList.login_id]
            emsg.subject = "Forget Password"
            mailResponse = EmailService.send(emsg, "forgotPassword", userList)
            if (mailResponse == 1):
                self.form["error"] = False
                self.form["message"] = "Please check your mail, Your password is send successfully"
                request.session["user"] = userList
                res = JsonResponse({"form": self.form})
            else:
                self.form["error"] = True
                self.form["message"] = "Please Check Your Internet Connection"
                res = JsonResponse({"form": self.form})
        else:
            self.form["error"] = True
            self.form["message"] = "login id is not correct"
            res = JsonResponse({"form": self.form})
        return res

    def input_validation(self):
        super().input_validation()
<<<<<<< HEAD
        inputError =  self.form["inputError"]
        if(DataValidator.isNull(self.form["login_id"])):
=======
        inputError = self.form["inputError"]
        if (DataValidator.isNull(self.form["login_id"])):
>>>>>>> 4dda84088e1d455acca1459810c682ff83a41715
            inputError["login_id"] = "Login can not be null"
            self.form["error"] = True
        if (DataValidator.isNull(self.form["password"])):
            inputError["password"] = "Password can not be null"
            self.form["error"] = True

        return self.form["error"]

    # Template html of Role page    
    def get_template(self):
        pass

    # Service of Role     
    def get_service(self):
        return UserService()
