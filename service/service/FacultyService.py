from service.models import Faculty
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection

'''
It contains Student business logics.
'''


class FacultyService(BaseService):
    def search(self, params):
        pageNo = (params["pageNo"] - 1) * self.pageSize
        sql = "select * from sos_faculty where 1=1"
        val = params.get("email", None)
        if DataValidator.isNotNull(val):
            sql += " and email = '" + val + "' "
        sql += " limit %s,%s"
        cursor = connection.cursor()

        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = (
            "id", "firstName", "lastName", "email", "password","mobileNumber", "address", "gender", "dob", "college_ID",
            "subject_ID", "course_ID")
        res = {
            "data": []
        }
        count = 0
        for x in result:
            res["data"].append({columnName[i]: x[i] for i, _ in enumerate(x)})
        return res

    def get_model(self):
        return Faculty
