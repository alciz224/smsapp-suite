from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, RedirectView

from people.mixins import UserInfoMixin
from user.forms import MyUserCreationForm, MyLoginForm, CombinedForm
from user.models import CustomUser

class MyUserCreateView(CreateView):
    form_class = MyUserCreationForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('user_login')

class MyLoginView(LoginView):
    form_class = MyLoginForm
    template_name = 'user/login_page.html'

class MyLogoutView(LogoutView):
    next_page = 'user_login'

class UserHomeView(UserInfoMixin,TemplateView):
    template_name = 'people/admin/home.html'

class StudentHomeView(UserInfoMixin, TemplateView):

    template_name = 'people/student/student_home.html'

class TeacherHomeView(UserInfoMixin,TemplateView):
    template_name = 'people/teacher/teacher_home.html'

class SAHomeView(UserInfoMixin,TemplateView):
    template_name = 'people/schooladmin/school_admin_home.html'

class HomeRedirectView(RedirectView):

    def get_user_model(self):
        return CustomUser

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            user_type = self.request.user.user_type
            if user_type=='STUDENT':
                return reverse('student_home')
            elif user_type=='TEACHER':
                return reverse('teacher_home')
            elif user_type=='SCHOOLADMIN':
                return reverse('schoolyearselect')
            elif user_type=='ADMIN':
                return reverse('user_home')

        else:
            return reverse('user_login')