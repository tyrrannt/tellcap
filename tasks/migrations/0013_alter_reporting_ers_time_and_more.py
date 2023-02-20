# Generated by Django 4.1.4 on 2022-12-21 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0012_task_create_reporting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporting',
            name='ers_time',
            field=models.DateField(blank=True, null=True, verbose_name='Старт времени оценки экзаменатора'),
        ),
        migrations.AlterField(
            model_name='reporting',
            name='first_rss_time',
            field=models.DateField(blank=True, null=True, verbose_name='Старт времени оценки первого рейтера'),
        ),
        migrations.AlterField(
            model_name='reporting',
            name='second_rss_time',
            field=models.DateField(blank=True, null=True, verbose_name='Старт времени оценки второго рейтера'),
        ),
    ]
