# Generated by Django 3.1.5 on 2021-04-20 12:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('tests', '0005_test_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='short_desc',
        ),
        migrations.AlterField(
            model_name='test',
            name='created',
            field=models.DateField(auto_created=True, verbose_name='Дата создания'),
        ),
    ]
