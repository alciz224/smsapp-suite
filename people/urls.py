from django.urls import path

from people.views import StudentUpdateView, StudentDetailView
from user.views import MyLoginView, MyUserCreateView, UserHomeView, MyLogoutView, HomeRedirectView, StudentHomeView, \
    TeacherHomeView, SAHomeView

urlpatterns = [
    path('student/<int:pk>', StudentDetailView.as_view(), name='student_detail'),
    path('student/update/<int:pk>', StudentUpdateView.as_view(), name='student_update'),
    path('student/request', MyLoginView.as_view(), name='user_login'),

]