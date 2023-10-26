from django.urls import path
from people.views import StudentHomeView, StudentUpdateView, StudentDetailView, StudentClassroomView, TeacherHomeView, \
    SAHomeView, \
    UserHomeView, SchoolYearSelect, StudentMarksView, StudentAverageView, StudentTimeTableView

from user.views import MyLoginView

urlpatterns = [
    #-----------STUDENT URLS-------------
    path('student-home', StudentHomeView.as_view(), name='student_home'),
    path('student/<int:pk>', StudentDetailView.as_view(), name='student_detail'),
    path('student/update/<int:pk>', StudentUpdateView.as_view(), name='student_update'),
    path('student-classroom', StudentClassroomView.as_view(), name='student_classroom'),
    path('student-marks', StudentMarksView.as_view(), name='student_marks'),
    path('student-average', StudentAverageView.as_view(), name='student_average'),
    path('student-timetable', StudentTimeTableView.as_view(), name='student_timetable'),

    #-----------TEACHER URLS-------------
    path('teacher-home', TeacherHomeView.as_view(), name='teacher_home'),
    # path('teacher/<int:pk>', TeacherDetailView.as_view(), name='teacher_detail'),
    # path('teacher/update/<int:pk>', TeacherUpdateView.as_view(), name='teacher_update'),
    # path('teacher/classrooms', TeacherClassroomListView.as_view(), name='teacher_classrooms'),
    # path('teacher/classrooms', TeacherClassroomListView.as_view(), name='teacher_classrooms'),
    # path('teacher/classrooms', TeacherClassroomListView.as_view(), name='teacher_classrooms'),
    #-----------SCHOOL ADMIN URLS-------------
    path('sa-home', SAHomeView.as_view(), name='school_admin_home'),
    #-----------ADMIN URLS-------------
    path('admin-home', UserHomeView.as_view(), name='user_home'),
    path('select-school-year', SchoolYearSelect.as_view(), name='schoolyearselect')


]