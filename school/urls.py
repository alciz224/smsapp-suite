from django.urls import path

from school.views import ScheduleCreateView, ScheduleListView, TimeTableCreateView, TimeTableListView, timetable_create

urlpatterns = [
    path('schedule-create', ScheduleCreateView.as_view(), name='schedule_create'),
    path('schedule-list', ScheduleListView.as_view(), name='schedule_list'),
    path('timetable-create', timetable_create, name='timetable_create'),
    path('timetable-list', TimeTableListView.as_view(), name='timetable_list'),


]