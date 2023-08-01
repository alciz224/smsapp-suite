from django.urls import path

from school.views import ScheduleCreateView, ScheduleListView

urlpatterns = [
    path('schedule-create', ScheduleCreateView.as_view(), name='student_detail'),
    path('schedule-list', ScheduleListView.as_view(), name='student_update'),


]