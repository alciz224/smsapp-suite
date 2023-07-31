from django.shortcuts import render

# Create your views here.
from django.views.generic import CreateView

from school.models import MonthlySchedule


class ScheduleCreateView(CreateView):
    model = MonthlySchedule
    fields = ['name', 'school', 'is_current']
    template_name = 'school/schedule_create.html'

