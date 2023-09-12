
from django.contrib.auth.views import LoginView, LogoutView
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView


from user.forms import MyUserCreationForm, MyLoginForm


class MyUserCreateView(CreateView):
    form_class = MyUserCreationForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('user_login')

class MyLoginView(LoginView):
    form_class = MyLoginForm
    template_name = 'user/login_page.html'

class MyLogoutView(LogoutView):
    next_page = 'user_login'



