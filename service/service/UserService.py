from django.db import connection

from service.models import User
from service.utility.DataValidator import DataValidator
from .BaseService import BaseService

'''
It contains User business logics.   
'''


class UserService(BaseService):

    def authenticate(self, params):
        userList = self.get_model().objects.filter()
        if userList.count() > 0:
            for userData in userList:
                if params['login_id'] == userData.login_id and params['password'] == userData.password:
                    return userData
        else:
            return None

    def search(self, params):

        pageNo = (params["pageNo"] - 1) * self.pageSize
        sql = "select * from sos_user where 1=1"
        val = params.get("login_id", None)
        if DataValidator.isNotNull(val):
            sql += " and login_id = '" + val + "' "
        sql += " limit %s,%s"
        cursor = connection.cursor()
        cursor.execute(sql, [pageNo, self.pageSize])
        result = cursor.fetchall()
        columnName = (
        "id", "firstName", "lastName", "login_id", "password", "confirmpassword", "dob", "address", "gender",
        "mobilenumber", "role_Id", "role_Name")
        res = {
            "data": []
        }
        count = 0
        for x in result:
            res["data"].append({columnName[i]: x[i] for i, _ in enumerate(x)})
        return res

    def get_login_id(self, login):
        q = self.get_model().objects.filter()
        if (DataValidator.isNotNull(login)):
            q = q.filter(login_id=login)
        return q



    def get_model(self):
        return User
