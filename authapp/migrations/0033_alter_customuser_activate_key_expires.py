# Generated by Django 4.1.7 on 2024-05-02 12:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authapp", "0032_alter_customuser_activate_key_expires"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="activate_key_expires",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 5, 4, 12, 14, 41, 464213, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]