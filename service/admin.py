from django.contrib import admin

# Register your models here.
from .models import Role, User, College, Marksheet, Student, Faculty, TimeTable, Subject, Course

admin.site.register(Role)
admin.site.register(User)
admin.site.register(College)
admin.site.register(Course)
admin.site.register(Marksheet)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(TimeTable)
