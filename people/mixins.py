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
            context['profile'] = profile

        elif self.request.user.user_type == 'ADMIN':
            profile = WebAdmin.objects.get(user=self.request.user)
            context['profile'] = profile
        elif self.request.user.user_type == 'TEACHER':
            profile = Teacher.objects.get(user=self.request.user)
            context['profile'] = profile
        elif self.request.user.user_type == 'STUDENT':
            profile = Student.objects.get(user=self.request.user)
            context['profile'] = profile
            context['schoolyears'] = SchoolYear.objects.filter(level__schoolyearstudent__student=profile)
            context['school_year'] = self.request.session.get('school_year')
            context['next'] = self.request.session.get('next')
            if context['school_year']:
                context['current_year_student'] = SchoolYearStudent.objects.get(level_id=int(context['school_year']),
                                                                                student=profile)

            print(list(context['schoolyears'].values_list('id', flat=True)))




        else:
            profile = None
            context['profile'] = profile



        return context

