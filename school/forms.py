from django import forms

from school.models import TimeTable


class TimeTableCreateForm(forms.ModelForm):

    class Meta:
        model = TimeTable
        fields = ['schedule', 'start_time', 'end_time', 'day', 'subject', 'classroom']

