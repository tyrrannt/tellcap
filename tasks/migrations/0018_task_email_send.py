# Generated by Django 4.1.4 on 2023-01-12 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0017_alter_task_visible_date_end_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='email_send',
            field=models.BooleanField(default=False, verbose_name='Отправлено письмо'),
        ),
    ]
