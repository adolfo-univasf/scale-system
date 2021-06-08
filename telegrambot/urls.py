from django.urls import path

from . import views

app_name = 'telegrambot'

urlpatterns = [
    path('<int:id>/', views.menu,  name='menu'),
    path('program/', views.program,  name='program'),
    path('confirm/<int:id>/<int:code>', views.verification,  name='verification'),
    
]