from django.shortcuts import render
from django.views import View


def homeView(request):
    return render(request, 'main_welcome.html')
