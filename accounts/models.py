import re

from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext as _

from django.conf import settings
from django.contrib.auth.models import Group

leader_group, created = Group.objects.get_or_create(name='Leader')
treasurer_group, created = Group.objects.get_or_create(name='Treasurer')
elder_group, created = Group.objects.get_or_create(name='Elder')

"""
doctor_group.permissions.set([permission_list])
doctor_group.permissions.add(permission, permission, ...)
doctor_group.permissions.remove(permission, permission, ...)
doctor_group.permissions.clear()

doctor_group.user_set.add(user)
            OR
user.groups.add(doctor_group)
"""

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('User Name'), max_length=30, unique=True,
        validators = [validators.RegexValidator(re.compile('^[\w.@+-]+$'), 
            'O nome de usuário não pode conter letras, digitos ou os seguintes caracteres: @/./+/-/+')])
    email = models.EmailField(_('E-mail'), unique=True)
    name = models.CharField(_('Name'), max_length=100, blank=True)
    telefone = PhoneNumberField(_("Telegram Phone Number"), blank=True)
    name_telegram = models.SlugField(_("Telegram User Name"), blank=True)
    id_telegram = models.SlugField(_("Telegram ID"), blank=True)
    is_active = models.BooleanField(_('Is Active?'), blank=True, default=True)
    is_staff = models.BooleanField(_('Is Staff?'), blank=True, default=False)
    date_joined = models.DateTimeField(_('Entry date'), auto_now_add = True)
    first_access = models.BooleanField(_('Already logged in?'), blank=True, default=False)

    objects = UserManager()

    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.name or self.username

    def get_short_name(self):
        return self.username
    def get_full_name(self):
        return str(self)
    
    class Meta:
        verbose_name= 'Usuário'
        verbose_name_plural = 'Usuários' 

class PasswordReset(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Usuário',
        related_name='resets', on_delete=models.CASCADE
    )
    key = models.CharField(_('Key'), max_length=100, unique=True)
    created_at = models.DateTimeField(_('Created on'), auto_now_add=True)
    confirmed = models.BooleanField(_('Confirmed?'), default=False, blank=True)

    def __str__(self):
        return '{0} em {1}'.format(self.user, self.created_at)

    class Meta:
        verbose_name = 'Nova Senha'
        verbose_name_plural = 'Novas Senhas'
        ordering = ['-created_at']