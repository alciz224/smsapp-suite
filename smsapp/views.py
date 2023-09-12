from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import RedirectView

from user.models import CustomUser


def homeView(request):
    return render(request, 'main_welcome.html')

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


