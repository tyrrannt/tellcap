from django.contrib import admin

# Register your models here.
from tasks.models import Task, Reporting, FileUpload

admin.site.register(Task)
admin.site.register(Reporting)
admin.site.register(FileUpload)

