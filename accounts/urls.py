from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.dashboard,  name='dashboard'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'),  name='login'),
    path('logout/', LogoutView.as_view(next_page = 'core:home'),  name='logout'),
    path('sign/', views.register,  name='register'),
    path('edit/', views.edit,  name='edit'),
    path('password-edit/', views.edit_password,  name='edit_password'),
    path('reset-password/', views.password_reset,  name='password_reset'),
    path('reset-password-confirm/<slug:key>', views.password_reset_confirm,  name='password_reset_confirm'),
]