from django.http import HttpResponse
from abc import ABC,abstractmethod
from django.shortcuts import render,redirect

'''
Base class is inherited by all application controllers 
'''
class BaseCtl(ABC):

    #Contains preload data
    preload_data = {}

    #Contains list of objects, it will be displayed at list page 
    page_list = {}

    '''
    Initialize controller attributes
    '''
    def __init__(self):
        self.form = {}
        self.form["pageNo"] = 1
        self.form["id"] = 0
        self.form["message"] = ""
        self.form["error"] = False
        self.form["inputError"] = {}
        self.form["data"] = {}
        self.form["sessionKey"] = ""

    '''
    It loads preload data of the page 
    '''
    def preload(self,request):
        print("This is preload")

    '''
    Displays rceord of received ID    
    '''
    def display(self,request,params = {}):
        pass 

    '''
    Submit data 
    '''
    def submit(self,request,params = {}):
        pass      

    '''
    Populate values from Request POST/GET to Controller form object
    '''
    def request_to_form(self,requestFrom):
        pass

    #Populate Form from Model 
    def model_to_form(self,obj):
        pass

    #Convert form into module
    def form_to_model(self,obj):
        pass        

    '''
    Apply input validation 
    '''        
    def input_validation(self):
        self.form["error"] = False
        self.form["message"] = ""

    '''
    returns template of controller
    '''    
    def get_template(self):
        pass

    def get_service(self):
        pass
