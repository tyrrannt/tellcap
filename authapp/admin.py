from django.contrib import admin
from authapp.models import CustomUser, Organisation, BugReport
# Register your models here.
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    """
    Расширяем модель UserAdmin
    fieldsets: исходный набор полей формы
    *UserAdmin.fieldsets: добавляем расширенный набор полей формы,
        тип: кортеж содержащий ('заголовок группы по вашему выбору', {словарь c новыми полями})
    """
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Профиль',
            {
                'fields': (
                    'surname', 'superintendent', 'personal_code', 'organisation',
                ),
            },
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Organisation)
admin.site.register(BugReport)
