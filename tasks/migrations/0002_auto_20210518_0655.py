# Generated by Django 3.1.5 on 2021-05-18 06:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='visible_date',
        ),
        migrations.AddField(
            model_name='task',
            name='visible_date_end',
            field=models.DateField(default=datetime.datetime(2021, 5, 18, 6, 55, 22, 737547), verbose_name='Дата окончания'),
        ),
        migrations.AddField(
            model_name='task',
            name='visible_date_start',
            field=models.DateField(default=datetime.datetime(2021, 5, 18, 6, 55, 22, 737518), verbose_name='Дата начала'),
        ),
    ]
