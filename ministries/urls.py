from django.urls import path

from . import views

app_name = 'ministries'

urlpatterns = [
    path('', views.dashboard,  name='dashboard'),
    path('register', views.register,  name='register'),
    path('all', views.all,  name='all'),
    path('<slug:ministry>', views.description,  name='description'),
    path('<slug:ministry>/edit', views.edit,  name='edit'),
]