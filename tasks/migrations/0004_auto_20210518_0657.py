# Generated by Django 3.1.5 on 2021-05-18 06:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_auto_20210518_0656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='visible_date_end',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Дата окончания'),
        ),
        migrations.AlterField(
            model_name='task',
            name='visible_date_start',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Дата начала'),
        ),
    ]
