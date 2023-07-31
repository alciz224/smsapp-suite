from django.shortcuts import render

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView, DetailView

from people.forms import ProfileForm
from people.mixins import UserInfoMixin
from people.models import Student


class StudentDetailView(UserInfoMixin, DetailView):
    model = Student
    context_object_name = 'student'
    template_name = 'people/student/student_detail.html'


class StudentUpdateView(UserInfoMixin, UpdateView):
    model = Student
    fields = ['image']
    template_name = 'people/student/student_profile_update.html'
    success_url = reverse_lazy('student_home')
