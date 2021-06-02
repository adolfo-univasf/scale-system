from django.urls import path

from . import views

app_name = 'programs'

urlpatterns = [
    path('', views.dashboard,  name='dashboard'),
    path('register', views.register,  name='register'),
    path('all', views.all,  name='all'),
    path('<int:program>', views.description,  name='description'),
    path('<int:program>/program', views.program,  name='program'),
]