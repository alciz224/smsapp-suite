import datetime

from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from school.models import TimeTable


class TimeTableCreateForm(forms.ModelForm):

    class Meta:
        model = TimeTable
        fields = ['schedule', 'start_time', 'end_time', 'day', 'subject', 'classroom']

    start_time = forms.TimeField(

        widget=forms.TimeInput(attrs={'type': 'time', 'id': 'startTime', 'step': '900', 'min': '07:00', 'max': '18:30'}), input_formats=['%H:%M'],
        validators=[
            MinValueValidator(datetime.time(7, 0)),
            MaxValueValidator(datetime.time(18, 30))
        ]
    )
    end_time = forms.TimeField(

        widget=forms.TimeInput(attrs={'type': 'time', 'id': 'endtTime', 'step': '900', 'min': '08:00', 'max': '18:30'}, format='%H:%M',),
        input_formats=['%H:%M'],
        validators=[
            MinValueValidator(datetime.time(8, 0)),
            MaxValueValidator(datetime.time(18, 30))
        ]
    )