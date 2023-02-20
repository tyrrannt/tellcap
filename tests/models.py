from ckeditor.fields import RichTextField
from django.db import models

# Create your models here.
from django.urls import reverse

from authapp.models import CustomUser


class Category(models.Model):
    """
        Модель категориий
    """

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'

    name = models.CharField(verbose_name='Наименование', max_length=64, unique=True)
    description = models.TextField(verbose_name='Описание', blank=True)
    is_active = models.BooleanField(db_index=True, verbose_name='Активна', default=True)

    def __str__(self):
        """
        Переопределение стандартного метода str
        :return: Возвращает заданное пользователем представление экземпляра класса
        """
        return self.name

    def get_absolute_url(self):
        return reverse('tests:view_category', kwargs={"pk": self.pk})


class Test(models.Model):

    class Meta:
        verbose_name_plural = 'Файлы'
        verbose_name = 'Файл'

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(verbose_name='Наименование', max_length=64, unique=True)
    description = RichTextField(verbose_name='Описание', blank=True)
    is_active = models.BooleanField(db_index=True, verbose_name='Активна', default=True)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    created = models.DateField(verbose_name='Дата создания', auto_created=True, null=False)

    def __str__(self):
        """
        Переопределение стандартного метода str
        :return: Возвращает заданное пользователем представление экземпляра класса
        """
        return self.name

    def get_absolute_url(self):
        return reverse('tests:view_test', kwargs={"pk": self.pk})
