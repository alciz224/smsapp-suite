from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from user.models import CustomUser


class MyUserCreationForm(UserCreationForm):
    USER_TYPES_CHOICES = (
        ('STUDENT', 'Student'),
        ('TEACHER', 'Teacher'),
    )
    user_type = forms.ChoiceField(choices=USER_TYPES_CHOICES, required=True)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'user_type']


class MyLoginForm(AuthenticationForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = CustomUser

class CombinedForm(forms.Form):
    login_form = MyLoginForm()
    registration_form = MyUserCreationForm()