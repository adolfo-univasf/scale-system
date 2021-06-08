from django.urls import path

from . import views

app_name = 'telegrambot'

urlpatterns = [
    path('', views.dashboard,  name='dashboard'),
    path('program/', views.program,  name='program'),
    
]