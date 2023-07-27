from django.contrib import admin

# Register your models here.
from people.models import WebAdmin, Student, Teacher, SchoolAdmin

admin.site.register(WebAdmin)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(SchoolAdmin)