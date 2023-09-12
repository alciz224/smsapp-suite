from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView, DetailView, TemplateView

from people.forms import ProfileForm
from people.mixins import UserInfoMixin
from people.models import Student
from school.models import SchoolYear, Classroom


class SchoolYearSelect(UserInfoMixin, TemplateView):

    def post(self, request):
        school_year = int(request.POST.get('school_year'))
        context = self.get_context_data()
        link = request.session.get('next', '/')
        if school_year in list(context['schoolyears'].values_list('id', flat=True)):
            print('ok')
            request.session['school_year'] = school_year
            return HttpResponseRedirect(link)
        else:
            error_message = 'Invalid school year'
            context = self.get_context_data()
            context['error_message'] = error_message
            return render(request, 'people/student/school_year_select.html', context)


    template_name = 'people/student/school_year_select.html'

#---------------------STUDENT VIEWS---------------------

class StudentHomeView(UserInfoMixin, TemplateView):
    def dispatch(self, request, *args, **kwargs):
        school_year = request.session.get("school_year")
        link = request.get_full_path()
        if school_year is None:
            request.session['next'] = link
            return redirect("schoolyearselect")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['school_year']  = self.request.session.get('school_year')
        return context

    template_name = 'people/student/student_home.html'

class StudentDetailView(UserInfoMixin, DetailView):
    model = Student
    context_object_name = 'student'
    template_name = 'people/student/student_detail.html'


    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.user_type == 'STUDENT'

    def handle_no_permission(self):
        return HttpResponse('access denied!!!!')


class StudentUpdateView(UserInfoMixin, UserPassesTestMixin, UpdateView):
    model = Student
    fields = ['image']
    template_name = 'people/student/student_profile_update.html'
    success_url = reverse_lazy('student_home')

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.user_type == 'STUDENT'

    def handle_no_permission(self):
        return HttpResponse('access denied!!!!')

class StudentClassroomView(UserInfoMixin, TemplateView):
    def get_queryset(self):
        context = self.get_context_data()
        stud = context['current_year_student']
        classroom = stud.classroom.id
        queryset = Classroom.objects.get(id=classroom)
        return queryset

    context_object_name = 'classroom'
    template_name = 'people/student/student_classroom.html'
    success_url = reverse_lazy('student_home')

#-----------------TEACHER VIEWS----------------------------------
class TeacherHomeView(UserInfoMixin,TemplateView):
    template_name = 'people/teacher/teacher_home.html'

class TeacherDetailView(UserInfoMixin,TemplateView):
    template_name = 'people/teacher/teacher_detail.html'

class TeacherUpdateView(UserInfoMixin,TemplateView):
    template_name = 'people/teacher/teacher_update.html'






#-----------------SCHOOL ADMIN VIEWS----------------------------------
class SAHomeView(UserInfoMixin,TemplateView):
    template_name = 'people/schooladmin/school_admin_home.html'

class SADetailView(UserInfoMixin,TemplateView):
    template_name = 'people/teacher/school_admin_detail.html'

class SAUpdateView(UserInfoMixin,TemplateView):
    template_name = 'people/teacher/school_admin_update.html'


#-----------------SCHOOL ADMIN VIEWS----------------------------------
class UserHomeView(UserInfoMixin,TemplateView):
    template_name = 'people/admin/home.html'

class AdminHomeView(UserInfoMixin,TemplateView):
    def dispatch(self, request, *args, **kwargs):
        school_year = request.session.get("school_year")
        if school_year is None:
            return redirect("schoolyearselect")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['school_year']=self.request.session.get('school_year')
        return context
    template_name = 'people/schooladmin/school_admin_home.html'

class AdminDetailView(UserInfoMixin,TemplateView):
    template_name = 'people/teacher/admin_detail.html'

class AdminUpdateView(UserInfoMixin,TemplateView):
    template_name = 'people/teacher/admin_update.html'
