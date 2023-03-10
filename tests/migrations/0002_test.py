# Generated by Django 3.1.5 on 2021-02-22 12:22

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('tests', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Наименование')),
                ('description', ckeditor.fields.RichTextField(blank=True, verbose_name='Описание')),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='Активна')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.category')),
            ],
        ),
    ]
