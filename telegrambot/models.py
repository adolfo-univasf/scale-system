from django.db import models
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings

# Create your models here.


class TelegramAccount(models.Model):
    user = models.ForeignKey("accounts.User", verbose_name=_("User"), on_delete=models.CASCADE, related_name=_('PhoneUser'))
    id_telegram = models.SlugField(_("Telegram ID"), blank=True, null=True, unique=True)
    name_telegram = models.SlugField(_('Telegram Username'),max_length=30,blank=True, null=True)
    def __str__(self):
        return '{0} {1}'.format(self.user, self.id_telegram)
    class Meta:
        verbose_name= _('Telegram Account')
        verbose_name_plural = _('Telegram Accounts')
        ordering = ['user','id_telegram']
    

class VerificationCode(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Usuário',
        related_name='confirm_telegram', on_delete=models.CASCADE
    )
    confirmed = models.BooleanField(_('Confirmed?'), default=False, blank=True)
    created_at = models.DateTimeField(_('Created on'), auto_now_add=True)
    def __str__(self):
        return '{0} em {1}'.format(self.user, self.created_at)
