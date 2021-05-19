# Generated by Django 3.2 on 2021-05-19 12:33

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id_telegram',
            field=models.SlugField(blank=True, verbose_name='Telegram ID'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name_telegram',
            field=models.SlugField(blank=True, verbose_name='Telegram User Name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='telefone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name='Telegram Phone Number'),
        ),
    ]
