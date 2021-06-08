from django.urls import path

from . import views

app_name = 'telegrambot'

urlpatterns = [
    path('<int:id>/', views.menu,  name='menu'),
    path('<int:id>/program/', views.program,  name='program'),
    path('<int:id>/confirm/<int:code>', views.verification,  name='verification'),
    
]