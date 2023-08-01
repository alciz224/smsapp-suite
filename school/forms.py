from django import forms

from school.models import MonthlySchedule, TimeTable


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = MonthlySchedule
        fields = ['name']

'''class TimeTableForm(forms.ModelForm):
    class Meta:
        model = TimeTable
        fields = ['__all__']'''

