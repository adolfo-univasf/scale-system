from django.urls import path

from . import views

app_name = 'telegrambot'

urlpatterns = [
    path('program/', views.program,  name='program'),
    
]