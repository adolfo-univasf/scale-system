from django.contrib import admin
from .models import TelegramAccount, VerificationCode

# Register your models here.

class TelegramAccountAdmin(admin.ModelAdmin):
    search_fields = ['user__username']

class VerificationCodeAdmin(admin.ModelAdmin):
    search_fields = ['user__username']

admin.site.register(TelegramAccount, TelegramAccountAdmin)
admin.site.register(VerificationCode, VerificationCodeAdmin)