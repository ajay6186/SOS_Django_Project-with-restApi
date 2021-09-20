


from service.models import Subject
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection
'''
It contains Student business logics.   
'''
class SubjectService(BaseService):
    
    def search(self,params):

        pageNo = (params["pageNo"]-1)*self.pageSize
        sql="select * from sos_subject where 1=1"
        val = params.get("subjectName", None)
        if DataValidator.isNotNull(val):
            sql+=" and subjectName = '"+val+"' "
        sql+=" limit %s,%s"
        cursor = connection.cursor()

        cursor.execute(sql,[pageNo,self.pageSize])
        result=cursor.fetchall()
        columnName=("id","subjectName","subjectDescription","course_ID","courseName")
        res={
            "data":[]
        }
        count=0
        for x in result:

            res["data"].append({columnName[i] :  x[i] for i, _ in enumerate(x)})
        return res


    def get_model(self):
        return Subject
