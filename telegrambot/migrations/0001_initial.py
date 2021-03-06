# Generated by Django 3.2 on 2021-06-08 13:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VerificationCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telefone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Telegram Phone Number')),
                ('name_telegram', models.SlugField(blank=True, null=True, verbose_name='Telegram User Name')),
                ('confirmed', models.BooleanField(blank=True, default=False, verbose_name='Confirmed?')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='confirm_telegram', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
        ),
        migrations.CreateModel(
            name='TelegramAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telefone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Telegram Phone Number')),
                ('name_telegram', models.SlugField(blank=True, null=True, verbose_name='Telegram User Name')),
                ('id_telegram', models.SlugField(blank=True, null=True, unique=True, verbose_name='Telegram ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='PhoneUser', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Telegram Account',
                'verbose_name_plural': 'Telegram Accounts',
                'ordering': ['user', 'name_telegram', 'telefone'],
            },
        ),
    ]
