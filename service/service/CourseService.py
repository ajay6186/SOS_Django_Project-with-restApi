from service.models import Course
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection

'''
It contains Course business logics.   
'''


class CourseService(BaseService):

    def search(self, params):
        pageNo = (params["pageNo"] - 1) * self.pageSize
        sql = "select * from sos_course where 1=1"
        val = params.get("courseName", None)
        if DataValidator.isNotNull(val):
            sql += " and courseName = '" + val + "' "
        sql += " limit %s,%s"

        cursor = connection.cursor()
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = ("id", "courseName", "courseDescription", "courseDuration")
        res = {
            "data": []
        }
        count = 0
        for x in result:
            res["data"].append({columnName[i]: x[i] for i, _ in enumerate(x)})
        return res

    def get_model(self):
        return Course
