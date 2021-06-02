from django.urls import path

from . import views

app_name = 'scales'

urlpatterns = [
    path('', views.dashboard,  name='dashboard'),
    path('<int:function>', views.scale,  name='scale'),
    #path('register', views.ministryregister,  name='register'),
]