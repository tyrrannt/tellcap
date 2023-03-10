# Generated by Django 4.1.4 on 2022-12-23 10:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0014_reporting_reporting_visible'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporting',
            name='first_reiter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='first_reiter_person', to=settings.AUTH_USER_MODEL, verbose_name='Рейтер'),
        ),
        migrations.AlterField(
            model_name='reporting',
            name='second_reiter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='second_reiter_person', to=settings.AUTH_USER_MODEL, verbose_name='Рейтер'),
        ),
    ]
