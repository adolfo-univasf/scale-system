from django.urls import path

from . import views

app_name = 'ministries'

urlpatterns = [
    path('', views.dashboard,  name='dashboard'),
    path('register', views.register,  name='register'),
    path('all', views.all,  name='all'),
    path('allfunctionsselect', views.all_functions_select_json,  name='all-functions-select'),
    path('<slug:ministry>', views.description,  name='description'),
    path('<slug:ministry>/edit', views.edit,  name='edit'),
    path('<slug:ministry>/leave', views.leave,  name='leave'),
    path('<slug:ministry>/leave/<int:function>', views.leave_function,  name='leave-function'),
    path('<slug:ministry>/join/<int:function>', views.join_function,  name='join-function'),
    path('<slug:ministry>/delete/<int:function>', views.delete_function,  name='delete-function'),
    path('<slug:ministry>/edit/<int:function>', views.edit_function,  name='edit-function'),
    path('<slug:ministry>/register', views.register_function,  name='register-function'),
]