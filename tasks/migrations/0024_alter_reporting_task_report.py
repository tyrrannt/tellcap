# Generated by Django 4.1.7 on 2024-02-18 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0023_alter_fileupload_file_field"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reporting",
            name="task_report",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="reporting",
                to="tasks.task",
                verbose_name="Задача",
            ),
        ),
    ]
