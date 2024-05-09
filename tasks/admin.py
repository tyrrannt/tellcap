from django.contrib import admin

# Register your models here.
from tasks.models import Task, Reporting, FileUpload, ExamRecord

admin.site.register(Task)
admin.site.register(FileUpload)
admin.site.register(ExamRecord)


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
