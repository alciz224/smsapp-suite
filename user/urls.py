from django.urls import path

from user.views import MyLoginView, MyUserCreateView, MyLogoutView


urlpatterns = [

    path('user-login', MyLoginView.as_view(), name='user_login'),
    path('user-logout', MyLogoutView.as_view(), name='user_logout'),
    path('user-create', MyUserCreateView.as_view(), name='user_create'),


]