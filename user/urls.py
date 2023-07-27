from django.urls import path

from user.views import MyLoginView, MyUserCreateView, UserHomeView, MyLogoutView, HomeRedirectView, StudentHomeView, \
    TeacherHomeView, SAHomeView

urlpatterns = [
    path('admin-home', UserHomeView.as_view(), name='user_home'),
    path('user-login', MyLoginView.as_view(), name='user_login'),
    path('user-logout', MyLogoutView.as_view(), name='user_logout'),
    path('user-create', MyUserCreateView.as_view(), name='user_create'),
    path('student-home', StudentHomeView.as_view(), name='student_home'),
    path('teacher-home', TeacherHomeView.as_view(), name='teacher_home'),
    path('sa-home', SAHomeView.as_view(), name='school_admin_home'),



]