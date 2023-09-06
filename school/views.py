import datetime

#import numpy as np
#import pandas as pd
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.

from django.views.generic import CreateView, ListView, UpdateView

from school.forms import TimeTableCreateForm
from school.models import MonthlySchedule, TimeTable, Classroom


class ScheduleCreateView(CreateView):

    model = MonthlySchedule
    fields = ['name', 'school', 'is_current']

    template_name = 'school/schedule_create.html'
    success_url = 'schedule-list'

class ScheduleListView(ListView):

    model = MonthlySchedule
    template_name = 'school/schedule_list.html'

class TimeTableCreateView(CreateView):
    form_class = TimeTableCreateForm
    model = TimeTable
#   fields = ['schedule', 'start_time', 'end_time', 'day', 'subject', 'classroom']

    template_name = 'school/timetable_create.html'
    success_url = 'timetable-list'


class TimeTableUpdateView(UpdateView):
    form_class = TimeTableCreateForm
    model = TimeTable
    success_url = 'timetable-list'
    template_name = 'school/timetable_update.html'

    
class TimeTableListView(ListView):
    model = TimeTable
    template_name = 'school/timetable_list.html'
    context_object_name = "timetable"










def timetable_create(request):
    form = TimeTableCreateForm()
    if request.method == 'POST':
        form = TimeTableCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('timetable_list')
        else:
            form = TimeTableCreateForm()
            messages.info(request, 'not valid')
            return render(request, 'school/timetable_create.html', {'form': form})

    return render(request, 'school/timetable_create.html', {'form': form})

