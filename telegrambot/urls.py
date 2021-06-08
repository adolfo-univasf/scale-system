from django.urls import path

from . import views

app_name = 'telegrambot'

urlpatterns = [
    path('', views.dashboard,  name='dashboard'),
    path('generate/', views.generate,  name='generate'),
    path('<int:id>/', views.menu,  name='menu'),
    path('<int:id>/program/', views.program,  name='program'),
    path('<int:id>/register/<int:code>', views.register,  name='register'),
    path('<int:id>/scale/', views.scale_list,  name='scale-list'),
    path('<int:id>/scale/<int:code>', views.scale,  name='scale'),
    path('<int:id>/schedule', views.schedule,  name='schedule'),
    
]