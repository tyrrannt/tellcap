# Generated by Django 4.1.4 on 2022-12-19 14:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0012_customuser_superintendent_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'Пользователя', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AddField(
            model_name='customuser',
            name='surname',
            field=models.CharField(blank=True, default='', max_length=25, verbose_name='Отчетство'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='activate_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 21, 14, 0, 6, 403682, tzinfo=datetime.timezone.utc)),
        ),
    ]
