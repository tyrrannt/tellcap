import datetime
from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone

# Create your models here.
from django.utils.timezone import now


class Organisation(models.Model):
    class Meta:
        verbose_name_plural = 'Организации'
        verbose_name = 'Организация'

    short_name = models.CharField(verbose_name='Наименование', max_length=150, default='', help_text='')
    full_name = models.CharField(verbose_name='Полное наименование', max_length=250, default='', help_text='')
    inn = models.CharField(verbose_name='ИНН', max_length=12, blank=True, default='', help_text='')
    kpp = models.CharField(verbose_name='КПП', max_length=9, blank=True, default='', help_text='')
    ogrn = models.CharField(verbose_name='ОГРН', max_length=13, blank=True, default='', help_text='')
    juridical_address = models.TextField(verbose_name='Юридический адрес', default='', blank=True)
    physical_address = models.TextField(verbose_name='Фактический адрес', default='', blank=True)

    def __str__(self):
        return f'{self.short_name}'


class CustomUser(AbstractUser):
    class Meta:
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователя'

    avatar = models.ImageField(upload_to='Аватар', blank=True)
    birthday = models.DateField(verbose_name='День рождения', blank=True, null=True)
    activate_key = models.CharField(verbose_name='Код активации', max_length=128, blank=True, null=True)
    activate_key_expires = models.DateTimeField(default=(now() + timedelta(hours=48)))
    superintendent = models.BooleanField(verbose_name='Руководитель', default=False)
    surname = models.CharField(verbose_name='Отчетство', max_length=25, default='', blank=True)
    personal_code = models.CharField(verbose_name='Персональный код', max_length=4, default='', blank=True)
    organisation = models.ForeignKey(Organisation, verbose_name='Организация', on_delete=models.SET_NULL, null=True,
                                     blank=True)

    def is_activate_key_expired(self):
        if now() <= self.activate_key_expires:
            return False
        return True

    def __str__(self):
        return f'{self.personal_code}'


class BugReport(models.Model):
    class Meta:
        verbose_name_plural = 'Сбои'
        verbose_name = 'Сбой'

    bug_report_user = models.ForeignKey(CustomUser, verbose_name='Пользователь', on_delete=models.SET_NULL, null=True,
                                        related_name='bug_user')
    bug_time = models.DateTimeField(auto_created=True, auto_now_add=True)
    subject = models.CharField(verbose_name='Тема сообщения', max_length=100, blank=True)
    description = models.TextField(verbose_name='Текст сообщения')
    answer = models.TextField(verbose_name='Ответ специалиста')

    def __str__(self):
        return f'{self.subject}'

    def get_absolute_url(self):
        return reverse('auth:bugreport_list')


@receiver(post_save, sender=BugReport)
def sd_email(sender, instance, **kwargs):
    from django.core.mail import send_mail
    try:
        if datetime.datetime.now(tz=timezone.utc).__gt__(instance.bug_time):
            print(datetime.datetime.now(tz=timezone.utc))
            print(instance.bug_time)
            print('БОЛЬШЕ')
        if 0 > 1:
            send_mail(instance.subject, instance.description, 'administrator@complang.ru', ['shakirov.vitaliy@gmail.com'])
    except Exception as _ex:
        print(_ex)
