# Generated by Django 3.1.5 on 2022-12-19 10:55

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0007_auto_20221219_0842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='activate_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 21, 10, 55, 26, 168423, tzinfo=utc)),
        ),
    ]
