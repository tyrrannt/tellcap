# Generated by Django 4.1.4 on 2022-12-19 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0007_auto_20210609_1906'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='test',
            options={'verbose_name': 'Файл', 'verbose_name_plural': 'Файлы'},
        ),
    ]
