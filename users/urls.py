from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path ('home', views.HomeView, name="home"),
    path('login_user', views.login_user, name="login"),
    path('logout_user', views.logout_user, name="logout"),
    path('register_user', views.register_user, name="register_user"),
]  
