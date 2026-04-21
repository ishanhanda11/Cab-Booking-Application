from django.contrib import admin
from .models import UserManager, User, Course, Department, Employee
# Register your models here.

admin.site.register(User)
admin.site.register(Course)
admin.site.register(Department)
admin.site.register(Employee)