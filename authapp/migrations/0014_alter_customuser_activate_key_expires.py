# Generated by Django 4.1.4 on 2022-12-20 17:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0013_alter_customuser_options_customuser_surname_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='activate_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 22, 17, 54, 41, 695409, tzinfo=datetime.timezone.utc)),
        ),
    ]
