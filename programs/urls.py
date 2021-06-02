from django.urls import path

from . import views

app_name = 'programs'

urlpatterns = [
    path('', views.dashboard,  name='dashboard'),
    path('register', views.register,  name='register'),
    path('all', views.all,  name='all'),
    path('past', views.past,  name='past'),
    path('next', views.next,  name='next'),
    path('<int:program>', views.description,  name='description'),
    path('<int:program>/program', views.program,  name='program'),
    path('<int:program>/edit', views.edit,  name='edit'),
]