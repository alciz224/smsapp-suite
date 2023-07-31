from django.contrib.auth.mixins import LoginRequiredMixin

from people.models import SchoolAdmin, WebAdmin, Teacher, Student



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
        else:
            profile = None
            context['profile'] = profile



        return context