from django.contrib import admin

# Register your models here.
from tasks.models import Task, Reporting, FileUpload, ExamRecord


@admin.register(ExamRecord)
class ExamRecordAdmin(admin.ModelAdmin):
    # какие поля будут отображаться
    list_display = ("audio",)
    # какие поля будут использоваться для поиска
    search_fields = ["audio", ]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # какие поля будут отображаться
    list_display = ("student_uuid", "examiner", "test_module", "visible_date_start", "visible_date_end",
                    "create_reporting", "email_send", "deleted")
    # какие поля будут использоваться для поиска
    search_fields = ["student_uuid", "test_module", "visible_date_start", "visible_date_end", ]
    # какие поля будут использоваться для фильтрации
    list_filter = (
        "create_reporting", "email_send", "deleted"
    )
    # какие поля будут в виде ссылок
    list_display_links = ("test_module", "student_uuid")
    # какие поля будут использоваться для сортировки
    ordering = ['-visible_date_start', ]
    # какие поля будут отображаться в списке
    # list_editable = ("type_trip", "cancellation")
    # сколько строк будут использоваться для постраничного отображения
    list_per_page = 100
    # показывать ли пустые значения
    empty_value_display = '-//-'
    # какие поля будут использоваться из других моделей, для уменьшения запросов
    list_select_related = ("examiner",)


@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    # какие поля будут отображаться
    list_display = ("file_field",)
    # какие поля будут использоваться для поиска
    search_fields = ["file_field", ]


@admin.register(Reporting)
class ReportingAdmin(admin.ModelAdmin):
    # какие поля будут отображаться
    list_display = ("task_report", "student_uuid", "examiner", "first_reiter", "second_reiter", "completed")
    # какие поля будут использоваться для поиска
    search_fields = ["student_uuid", ]
    # какие поля будут использоваться для фильтрации
    list_filter = (
        "completed",
    )
    # какие поля будут в виде ссылок
    list_display_links = ("task_report", "student_uuid")
    # какие поля будут использоваться для сортировки
    ordering = ['-ers_time_start', ]
    # какие поля будут отображаться в списке
    # list_editable = ("type_trip", "cancellation")
    # сколько строк будут использоваться для постраничного отображения
    list_per_page = 100
    # показывать ли пустые значения
    empty_value_display = '-//-'
    # какие поля будут использоваться из других моделей, для уменьшения запросов
    list_select_related = ("examiner", "first_reiter", "second_reiter",)
