from django.urls import path

from . import views

app_name = 'scales'

urlpatterns = [
    path('', views.dashboard,  name='dashboard'),
    path('confirm/<int:programtime>', views.confirm,  name='confirm'),
    path('<int:function>', views.scale,  name='scale'),
    path('<int:function>/edit', views.edit,  name='edit'),
    
]