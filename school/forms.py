import datetime

from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from school.models import TimeTable, Classroom


class TimeTableCreateForm(forms.ModelForm):
    day = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-select'}))
    subject = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-select'}))
    classroom = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-select'}), queryset=Classroom.objects.all())

    class Meta:
        model = TimeTable
        fields = ['schedule', 'start_time', 'end_time', 'day', 'subject', 'classroom']

    schedule = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-select'}))
    start_time = forms.TimeField(

        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'step': '900', 'min': '07:00', 'max': '18:30'}, format='%H:%M'),
        input_formats=['%H:%M'],
        validators=[
            MinValueValidator(datetime.time(7, 0)),
            MaxValueValidator(datetime.time(18, 30))
        ]
    )
    end_time = forms.TimeField(

        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'step': '900', 'min': '08:00', 'max': '18:30'}, format='%H:%M',),
        input_formats=['%H:%M'],
        validators=[
            MinValueValidator(datetime.time(8, 0)),
            MaxValueValidator(datetime.time(18, 30))
        ]
    )
