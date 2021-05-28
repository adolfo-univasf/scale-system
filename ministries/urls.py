from django.urls import path

from . import views

app_name = 'ministries'

urlpatterns = [
    path('', views.dashboard,  name='dashboard'),
    path('register', views.register,  name='register'),
]