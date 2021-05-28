# Generated by Django 3.2 on 2021-05-28 14:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ministries', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('SA', 'Sábado'), ('JA', 'Saturday afternoon'), ('WE', 'Quarta-feira'), ('SN', 'Domingo'), ('FR', 'Sexta-feira'), ('SP', 'Special'), ('WP', 'Week of Prayer')], max_length=2)),
                ('description', models.TextField(blank=True, verbose_name='Simple Description')),
                ('date', models.DateField(blank=True, null=True, verbose_name='Date')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
            ],
            options={
                'verbose_name': 'Program',
                'verbose_name_plural': 'Programs',
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='ProgramTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(blank=True, max_length=50, null=True, verbose_name='Description')),
                ('time', models.TimeField(blank=True, null=True, verbose_name='Hora')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('confirmmed', models.ManyToManyField(blank=True, related_name='confirmmed', to=settings.AUTH_USER_MODEL, verbose_name='Confirmmed')),
                ('function', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ministries.function', verbose_name='Function')),
                ('lookup', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='scales.programtime', verbose_name='Same as')),
                ('person', models.ManyToManyField(blank=True, related_name='person', to=settings.AUTH_USER_MODEL, verbose_name='Person')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scales.program', verbose_name='Program')),
            ],
            options={
                'verbose_name': 'Program Time',
                'verbose_name_plural': 'Program Times',
                'ordering': ['program__date', 'program__name', 'time'],
            },
        ),
    ]