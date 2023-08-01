from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.

from django.views.generic import CreateView, ListView, UpdateView

from school.forms import TimeTableCreateForm
from school.models import MonthlySchedule, TimeTable


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

    def form_valid(self, form):
        schedule = form.cleaned_data['schedule']
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']
        day = form.cleaned_data['day']
        subject = form.cleaned_data['subject']
        classroom = form.cleaned_data['classroom']

        duplicate = TimeTable.objects.filter(schedule=schedule,
                                             start_time__range=(start_time, end_time),
                                             day=day,
                                             classroom=classroom
                                             ).first()
        if duplicate:
            messages.info(self.request, f"une classe existe déjà entre {start_time} et {end_time}!"
                                        f"Vous pouvez la mettre à jour ou cliquer sur choisir un autre horaire")
            return redirect('timetable_update', duplicate.pk)

        return super().form_valid(form)


class TimeTableUpdateView(UpdateView):
    form_class = TimeTableCreateForm
    model = TimeTable
    success_url = 'timetable-list'
    template_name = 'school/timetable_update.html'


class TimeTableListView(ListView):
    model = TimeTable
    context_object_name = 'horaire'
    template_name = 'school/timetable_list.html'

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

