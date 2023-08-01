from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.

from django.views.generic import CreateView, ListView

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
    model = TimeTable
    fields = ['schedule', 'start_time', 'end_time', 'day', 'subject', 'classroom']

    template_name = 'school/timetable_create.html'
    success_url = 'timetable-list'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.kwargs.get('timetable_id'):
            self.timetable_to_update = get_object_or_404(TimeTable, id=self.kwargs['timetable_id'])
            return kwargs

        def form_valid(self, form):
            cleaned_data = form.cleaned_data

            if self.timetable_to_update:

                self.object = self.timetable_to_update
                self.object.schedule = cleaned_data['schedule_id']
                self.object.start_time = cleaned_data['start_time']
                self.object.end_time = cleaned_data['end_time']
                self.object.day = cleaned_data['day']
                self.object.subject = cleaned_data['subject_id']
                self.object.classroom = cleaned_data['classroom_id']

            else:
                similar_timetable = TimeTable.objects.filter(start_time__hour=cleaned_data['start_time']).first()
                if similar_timetable:
                    messages.info(self.request, 'Similar timetable found. You can update it below.')
                    return self.render_to_response(self.get_context_data(form=form, timetable_id=similar_timetable.id))
                self.object = TimeTable.objects.create(**cleaned_data)

            return super().form_valid(form)



class TimeTableListView(ListView):
    model = TimeTable
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

