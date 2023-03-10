# Generated by Django 4.1.4 on 2022-12-26 14:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0020_organisation_customuser_personal_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bugreport',
            name='bug_time',
            field=models.DateTimeField(auto_created=True, auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='activate_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 28, 14, 29, 34, 789854, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='physical_address',
            field=models.TextField(blank=True, default='', verbose_name='Фактический адрес'),
        ),
    ]
