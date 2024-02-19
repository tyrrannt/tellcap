import datetime
import os
import pathlib
from decouple import config
from django.core.mail import EmailMultiAlternatives
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from authapp.models import CustomUser
from tellcap.settings import BASE_DIR, EMAIL_HOST_USER
from tests.models import Test
from django.utils.timezone import now
from loguru import logger

logger.add("debug.json", format="{time} {level} {message}", level="DEBUG", rotation="10 MB", compression="zip",
           serialize=True)
date = now


class Task(models.Model):
    class Meta:
        verbose_name_plural = 'Задачи'
        verbose_name = 'Задача'

    test_module = models.ForeignKey(Test, verbose_name='Модуль', on_delete=models.SET_NULL, null=True)
    examiner = models.ForeignKey(CustomUser, verbose_name='Экзаменатор', on_delete=models.SET_NULL, null=True)
    student_uuid = models.CharField(verbose_name='Уникальный номер экзаменуемого', max_length=4, default='', blank=True)
    visible_date_start = models.DateTimeField(verbose_name='Дата начала', auto_now=False, default=date)
    visible_date_end = models.DateTimeField(verbose_name='Дата окончания', auto_now=False, default=date)
    create_reporting = models.BooleanField(verbose_name='Создать отчет', default=False)
    email_send = models.BooleanField(verbose_name='Отправлено письмо', default=False)
    deleted = models.BooleanField(verbose_name='Признак удаления', default=False)

    def __str__(self):
        new_format = "%Y-%m-%d"
        return f"{self.examiner} : с {self.visible_date_start.strftime(new_format)} по {self.visible_date_end.strftime(new_format)}"

    def get_absolute_url(self):
        return reverse('tasks:purpose_list')


def directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    dt = instance.task_report.visible_date_start
    return f'report/{dt.year}/{dt.month}/{dt.day}/{filename}'


class Reporting(models.Model):
    class Meta:
        verbose_name_plural = 'Отчеты'
        verbose_name = 'Отчет'

    task_report = models.OneToOneField(Task, verbose_name='Задача', on_delete=models.CASCADE, related_name='reporting')
    student_uuid = models.CharField(verbose_name='Уникальный номер экзаменуемого', max_length=4)
    exam_record = models.FileField(
        verbose_name='Аудиозапись',
        upload_to=directory_path,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=('mp3', 'm4a'))])
    examiner = models.ForeignKey(CustomUser, verbose_name='Экзаминатор', on_delete=models.SET_NULL, null=True,
                                 related_name='examiner_person')
    ers = models.FileField(verbose_name='Оценка экзаменатора', upload_to=directory_path, blank=True, validators=[FileExtensionValidator(allowed_extensions=('xlsx', 'xls',))])
    ers_time_start = models.DateField(verbose_name='Начало оценки экзаменатора', null=True, blank=True)
    ers_time_end = models.DateField(verbose_name='Окончание оценки экзаменатора', null=True, blank=True)
    first_reiter = models.ForeignKey(CustomUser, verbose_name='Рейтер', on_delete=models.SET_NULL, null=True,
                                     related_name='first_reiter_person', blank=True)
    first_reiter_email_send = models.BooleanField(verbose_name='Отправлено письмо', default=False)
    first_rss_time_start = models.DateField(verbose_name='Начало оценки первого рейтера', null=True, blank=True)
    first_rss_time_end = models.DateField(verbose_name='Окончание оценки первого рейтера', null=True, blank=True)
    rrs_first = models.FileField(verbose_name='Оценка рейтера 1', upload_to=directory_path, blank=True, validators=[FileExtensionValidator(allowed_extensions=('xlsx', 'xls',))])
    second_reiter = models.ForeignKey(CustomUser, verbose_name='Рейтер', on_delete=models.SET_NULL, null=True,
                                      related_name='second_reiter_person', blank=True)
    second_reiter_email_send = models.BooleanField(verbose_name='Отправлено письмо', default=False)
    second_rss_time_start = models.DateField(verbose_name='Начало оценки второго рейтера', null=True, blank=True)
    second_rss_time_end = models.DateField(verbose_name='Окончание оценки второго рейтера', null=True, blank=True)
    rrs_second = models.FileField(verbose_name='Оценка рейтера 2', upload_to=directory_path, blank=True, validators=[FileExtensionValidator(allowed_extensions=('xlsx', 'xls',))])
    completed = models.BooleanField(verbose_name='Завершён', default=False)
    reporting_visible = models.BooleanField(verbose_name='Видимость в списке', default=True)

    def get_absolute_url(self):
        return reverse('tests:task_report_edit', kwargs={'pk': self.pk})


@receiver(post_save, sender=Task)
def create_report(sender, instance, **kwargs):
    try:
        if instance.create_reporting:
            try:
                print(instance.visible_date_start.date())
                obj = Reporting.objects.get(task_report=instance.pk)
                obj.student_uuid = instance.student_uuid
                obj.examiner = instance.examiner
                obj.ers_time_start = instance.visible_date_start.date()
                obj.ers_time_end = instance.visible_date_end.date()
                obj.save()
            except Exception as _ex:
                new_report = Reporting(task_report=instance, examiner=instance.examiner,
                                       student_uuid=instance.student_uuid)
                new_report.save()
    except Exception as _ex:
        print(_ex)

    try:
        if not instance.email_send:
            new_format = "%Y-%m-%d"
            subject = f'Тестирование Tellcap'
            description = f'{instance.examiner.last_name} {instance.examiner.first_name} - Вы назначены экзаменатором. ' \
                          f'Дата тестирования: {instance.visible_date_start.strftime(new_format)}. ' \
                          f'Код тестируемого: {instance.student_uuid} '
            from django.core.mail import send_mail
            result_obj = send_mail(subject, description, EMAIL_HOST_USER,
                                   [instance.examiner.email, config('TO_COPY'), ])
            if result_obj == 1:
                task_obj = Task.objects.get(pk=instance.pk)
                task_obj.email_send = True
                task_obj.save()

    except Exception as _ex:
        print(_ex)


def rename(file_name, path_name, instance, pfx):
    try:
        if instance.exam_record:
            # Получаем расширение файла
            ext = file_name.split('.')[-1]
            dt = instance.task_report.visible_date_start
            print(dt)
            # Формируем уникальное окончание файла. Длинна в 7 символов. В окончании номер записи: рк, спереди дополняющие нули
            uid = str(dt.year) + str(dt.month) + str(dt.day) + '_' + str(
                instance.task_report.test_module.name) + '_' + str(instance.student_uuid) + pfx
            filename = f'{uid}.{ext}'
            if file_name:
                try:
                    pathlib.Path.rename(pathlib.Path.joinpath(BASE_DIR, 'media', path_name, file_name),
                                        pathlib.Path.joinpath(BASE_DIR, 'media', path_name, filename))
                except Exception as _ex0:
                    print(_ex0)
            instance.exam_record = f'report/{dt.year}/{dt.month}/{dt.day}/{filename}'
            if file_name != filename:
                print(filename, file_name, dt)
                instance.save()
                task_record = Task.objects.get(pk=instance.task_report.pk)
                task_record.visible_date_end = datetime.datetime.now(tz=timezone.utc)
                task_record.save()

    except Exception as _ex:
        print(_ex)


@receiver(post_save, sender=Reporting)
def change_filename(sender, instance, **kwargs):
    try:
        if instance.first_reiter and not instance.first_reiter_email_send:
            TO = instance.first_reiter.email
            TO_COPY = config('TO_COPY')
            SUBJECT = 'Тестирование Tellcap'
            try:
                current_context = {
                    'last_name': instance.first_reiter.last_name,
                    'first_name': instance.first_reiter.first_name,
                    'block_type': 'рейтером',
                    'time_start': instance.first_rss_time_start,
                    'student_uuid': instance.student_uuid,
                    'time_end': instance.first_rss_time_end,
                    'obj_link': f'https://corp.tellcap.ru/tests/reporting/{instance.pk}/',
                }
                print(f'https://corp.tellcap.ru/tests/reporting/{instance.pk}/')
                text_content = render_to_string('tasks/email_template.html', current_context)
                html_content = render_to_string('tasks/email_template.html', current_context)
                msg = EmailMultiAlternatives(SUBJECT, text_content, EMAIL_HOST_USER, [TO, TO_COPY, ])
                msg.attach_alternative(html_content, "text/html")
                res = msg.send()
                if res == 1:
                    task_obj = Reporting.objects.get(pk=instance.pk)
                    task_obj.first_reiter_email_send = True
                    task_obj.save()
            except Exception as e:
                print("Failed to send the mail..", e)

        if instance.second_reiter and not instance.second_reiter_email_send:
            TO = instance.second_reiter.email
            TO_COPY = config('TO_COPY')
            SUBJECT = 'Тестирование Tellcap'
            try:
                current_context = {
                    'last_name': instance.second_reiter.last_name,
                    'first_name': instance.second_reiter.first_name,
                    'block_type': 'рейтером',
                    'time_start': instance.second_rss_time_start,
                    'student_uuid': instance.student_uuid,
                    'time_end': instance.second_rss_time_end,
                    'obj_link': f'https://corp.tellcap.ru/tests/reporting/{instance.pk}/',
                }
                print(f'https://corp.tellcap.ru/tests/reporting/{instance.pk}/')
                text_content = render_to_string('tasks/email_template.html', current_context)
                html_content = render_to_string('tasks/email_template.html', current_context)
                msg = EmailMultiAlternatives(SUBJECT, text_content, EMAIL_HOST_USER, [TO, TO_COPY, ])
                msg.attach_alternative(html_content, "text/html")
                res = msg.send()
                if res == 1:
                    task_obj = Reporting.objects.get(pk=instance.pk)
                    task_obj.second_reiter_email_send = True
                    task_obj.save()
            except Exception as e:
                print("Failed to send the mail..", e)

    except Exception as _ex:
        print(_ex)

    try:
        # Получаем имя сохраненного файла
        file_name = pathlib.Path(instance.exam_record.name).name
        print(file_name)
        # Получаем путь к файлу
        path_name = pathlib.Path(instance.exam_record.name).parent
        print(path_name)
        rename(file_name, path_name, instance, '')

    except Exception as _ex:
        print(_ex)

    # try:
    #     # Получаем имя сохраненного файла
    #     file_name = pathlib.Path(instance.ers.name).name
    #
    #     # Получаем путь к файлу
    #     path_name = pathlib.Path(instance.ers.name).parent
    #
    #     rename(file_name, path_name, instance, 'ers')
    # except Exception as _ex:
    #     print(_ex)
    #
    # try:
    #     # Получаем имя сохраненного файла
    #     file_name = pathlib.Path(instance.rrs_first.name).name
    #
    #     # Получаем путь к файлу
    #     path_name = pathlib.Path(instance.rrs_first.name).parent
    #
    #     rename(file_name, path_name, instance, 'rrs1')
    # except Exception as _ex:
    #     print(_ex)
    #
    # try:
    #     # Получаем имя сохраненного файла
    #     file_name = pathlib.Path(instance.rrs_second.name).name
    #
    #     # Получаем путь к файлу
    #     path_name = pathlib.Path(instance.rrs_second.name).parent
    #
    #     rename(file_name, path_name, instance, 'rrs2')
    # except Exception as _ex:
    #     print(_ex)


class FileUpload(models.Model):
    file_field = models.FileField(verbose_name='MP3 файл', upload_to='')

    def get_absolute_url(self):
        return reverse('tasks:file_list')
    
    def delete(self, using=None, keep_parents=False):
        path = pathlib.Path.joinpath(BASE_DIR, 'media', self.file_field.name)
        try:
            os.remove(path)
        except FileNotFoundError:
            logger.error(f'Ошибка удаления файла {self.file_field.name}')
        return super().delete()
