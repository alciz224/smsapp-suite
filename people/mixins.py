from django.contrib.auth.mixins import LoginRequiredMixin

from people.models import SchoolAdmin, WebAdmin, Teacher, Student
from school.models import SchoolYear, SchoolYearStudent, Classroom


class UserInfoMixin(LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['user'] = {
            'username': self.request.user.username,
            'role': self.request.user.get_user_type_display()

        }
        if self.request.user.user_type == 'SCHOOLADMIN':
            profile = SchoolAdmin.objects.get(user=self.request.user)
            school = profile.school
            school_years = school.years
            school_year = self.request.session.get('school_year')
            context['profile'] = profile
            context['school'] = school
            context['school_years'] = school_years

            if school_year:
                context['school_year'] = school_year

        elif self.request.user.user_type == 'ADMIN':
            profile = WebAdmin.objects.get(user=self.request.user)
            context['profile'] = profile
        elif self.request.user.user_type == 'TEACHER':
            profile = Teacher.objects.get(user=self.request.user)
            school_years = SchoolYear.objects.filter(year__schoolyear__schoolyearteacher__teacher=profile)
            school_year = self.request.session.get('school_year')
            print('school_year', school_year)
            context['profile'] = profile
            context['school_years'] = school_years
            if school_year:
                context['school_year'] = school_year



        elif self.request.user.user_type == 'STUDENT':
            profile = Student.objects.get(user=self.request.user)
            school_years = SchoolYear.objects.filter(level__schoolyearstudent__student=profile)
            context['profile'] = profile
            context['school_years'] = school_years
            context['school_year'] = self.request.session.get('school_year')
            context['next'] = self.request.session.get('next')
            if context['school_year']:
                context['current_year_student'] = SchoolYearStudent.objects.get(level_id=int(context['school_year']),
                                                                                student=profile)

            print(list(context['school_years'].values_list('id', flat=True)))




        else:
            profile = None
            context['profile'] = profile



        return context



