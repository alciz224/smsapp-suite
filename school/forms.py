import datetime

from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from school.models import TimeTable, Classroom


class TimeTableCreateForm(forms.ModelForm):
    
    class Meta:
        model = TimeTable
        fields = '__all__'
