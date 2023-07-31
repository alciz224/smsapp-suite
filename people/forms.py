from django import forms

from people.models import People


class ProfileForm(forms.ModelForm):
    class Meta:
        model = People
        fields = ['image']