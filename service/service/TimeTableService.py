from django.db import connection

from service.models import TimeTable
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService

'''  
It contains Student business logics.   
'''


class TimeTableService(BaseService):

    def search(self, params):

        pageNo = (params["pageNo"] - 1) * self.pageSize
        sql = "select * from sos_timetable where 1=1"
        val = params.get("semester", None)
        if DataValidator.isNotNull(val):
            sql += " and semester = '" + val + "' "
        sql += " limit %s,%s"
        cursor = connection.cursor()
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ("id", "examTime", "examDate", "subject_ID", "course_ID", "semester")
        res = {
            "data": []
        }
        count = 0
        for x in result:
            res["data"].append({columnName[i]: x[i] for i, _ in enumerate(x)})
        return res

    def Duplicate(self, coursename, subjectname, examdate, examtime, Semester):
        duplicate_data = self.get_model().objects.filter(course_ID=coursename, subject_ID=subjectname,
                                                         examDate=examdate, examTime=examtime, semester=Semester)
        return duplicate_data

    def get_model(self):
        return TimeTable
