from django.contrib import admin

# Register your models here.
from school.models import School, SchoolYear, Level, LevelChoice, ClassroomList, ClassroomChoice, Classroom, \
    SubjectList, SubjectChoice, Subject, Year, SchoolYearStudent, SchoolYearTeacher, MarkType, Mark


class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'phone', 'email']

class YearAdmin(admin.ModelAdmin):
    list_display = ['__str__']

class SchoolYearAdmin(admin.ModelAdmin):
    list_display = ['school', 'year', 'is_active']


class LevelChoiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_high_school']

class LevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'school_year']



#CLASSROOM-----------------------

class ClassroomListAdmin(admin.ModelAdmin):

    list_display = ['name']



class ClassroomChoiceAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'level']

class ClassroomAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'level', 'section']


class SchoolYearStudentAdmin(admin.ModelAdmin):
    list_display = ['student', 'classroom', 'level']

class SchoolYearTeacherAdmin(admin.ModelAdmin):
    list_display = ['teacher',   'school_year']

#SUBJECTS-------------------

class SubjectListAdmin(admin.ModelAdmin):
    list_display = ['name']

class SubjectChoiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'level']

class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'classroom', 'coef', 'teacher']
    list_filter = ['classroom']


class MarkTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'max_mark', 'is_released']
    list_filter = ['level']

class MarkAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'mark_type', 'mark1_d', 'mark2_d']

class TimeTableAdmin(admin.ModelAdmin):
    list_display = ['day', 'start_time', 'end_time', 'subject', 'teacher']




admin.site.register(School, SchoolAdmin)
admin.site.register(SchoolYear, SchoolYearAdmin)
admin.site.register(MarkType, MarkTypeAdmin)
admin.site.register(Mark, MarkAdmin)
admin.site.register(LevelChoice, LevelChoiceAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(ClassroomList, ClassroomListAdmin)
admin.site.register(ClassroomChoice, ClassroomChoiceAdmin)
admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(SubjectList, SubjectListAdmin)
admin.site.register(SubjectChoice, SubjectChoiceAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Year, YearAdmin)
admin.site.register(SchoolYearStudent, SchoolYearStudentAdmin)
admin.site.register(SchoolYearTeacher, SchoolYearTeacherAdmin)
#admin.site.register(TimeTable, TimeTableAdmin)