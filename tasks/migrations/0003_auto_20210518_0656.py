# Generated by Django 3.1.5 on 2021-05-18 06:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20210518_0655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='visible_date_end',
            field=models.DateField(default=datetime.datetime(2021, 5, 18, 6, 56, 4, 562996), verbose_name='Дата окончания'),
        ),
        migrations.AlterField(
            model_name='task',
            name='visible_date_start',
            field=models.DateField(default=datetime.datetime(2021, 5, 18, 6, 56, 4, 562996), verbose_name='Дата начала'),
        ),
    ]
