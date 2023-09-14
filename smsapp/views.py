from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import RedirectView, TemplateView

from user.models import CustomUser


class HomeView(View):
    def get(self, request):
        context = {}
        context['home'] = 'bienvenue'
        return render(request, 'main_welcome.html', context)




class HomeRedirectView(LoginRequiredMixin, RedirectView):

    def get_user_model(self):
        return CustomUser

    def get_redirect_url(self, *args, **kwargs):

        user_type = self.request.user.user_type
        if user_type == 'STUDENT':
            return reverse('student_home')
        elif user_type == 'TEACHER':
            return reverse('teacher_home')
        elif user_type == 'SCHOOLADMIN':
            return reverse('schoolyearselect')
        elif user_type == 'ADMIN':
            return reverse('user_home')
        else:
            return reverse('home')



