# Generated by Django 3.2 on 2021-05-19 16:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scales', '0002_auto_20210519_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='function',
            name='overload',
            field=models.ManyToManyField(blank=True, null=True, to='scales.Function', verbose_name='Overload'),
        ),
        migrations.AlterField(
            model_name='function',
            name='people',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL, verbose_name='People'),
        ),
        migrations.AlterField(
            model_name='ministry',
            name='leader',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL, verbose_name='Leadership'),
        ),
        migrations.RemoveField(
            model_name='programtime',
            name='person',
        ),
        migrations.AddField(
            model_name='programtime',
            name='person',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL, verbose_name='Person'),
        ),
    ]
