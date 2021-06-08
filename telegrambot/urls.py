from django.urls import path

from . import views

app_name = 'telegrambot'

urlpatterns = [
    path('<int:id>/', views.menu,  name='menu'),
    path('<int:id>/program/', views.program,  name='program'),
    path('<int:id>/register/<int:code>', views.register,  name='register'),
    path('<int:id>/scale/', views.scale_list,  name='scale-list'),
    path('<int:id>/scale/<int:code>', views.scale,  name='scale'),
    
]