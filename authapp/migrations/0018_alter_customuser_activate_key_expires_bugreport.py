# Generated by Django 4.1.4 on 2022-12-23 11:46

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0017_alter_customuser_activate_key_expires'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='activate_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 25, 11, 46, 1, 416266, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='BugReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bug_time', models.DateTimeField(auto_created=True)),
                ('subject', models.CharField(blank=True, max_length=100, verbose_name='Тема сообщения')),
                ('description', models.TextField(verbose_name='Текст сообщения')),
                ('answer', models.TextField(verbose_name='Ответ специалиста')),
                ('bug_report_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Сбой',
                'verbose_name_plural': 'Сбои',
            },
        ),
    ]
