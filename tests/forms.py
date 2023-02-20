import datetime

from ckeditor.widgets import CKEditorWidget
from django import forms
from django.forms import Textarea, DateField, DateInput

from authapp.models import CustomUser
from tasks.models import Reporting, Task
from tests.models import Test, Category


class TestForm(forms.ModelForm):
    # description = forms.CharField(widget=CKEditorWidget())
    created = forms.DateTimeField(required=False, widget=DateInput(attrs={'type': 'datetime-local'}),
                                  initial=datetime.date.today(), localize=True)

    class Meta:
        model = Test
        fields = ['category', 'name', 'description', 'is_active', 'author']
        widgets = {
            'description': Textarea(attrs={'cols': 80, 'rows': 40}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'is_active']


class TaskReportAddForm(forms.ModelForm):
    task_report = forms.ModelChoiceField(queryset=Task.objects.all())
    task_report.widget.attrs.update(
        {'class': 'form-select', 'id': 'id_task_report', 'name': 'task_report', })
    examiner = forms.ModelChoiceField(queryset=CustomUser.objects.filter(is_active=True), required=False)
    examiner.widget.attrs.update(
        {'class': 'form-select', 'id': 'id_examiner', 'name': 'examiner', 'required': False})
    first_reiter = forms.ModelChoiceField(queryset=CustomUser.objects.filter(is_active=True), required=False)
    first_reiter.widget.attrs.update(
        {'class': 'form-select', 'id': 'id_second_reiter', 'name': 'first_reiter', 'required': False})
    second_reiter = forms.ModelChoiceField(queryset=CustomUser.objects.filter(is_active=True), required=False)
    second_reiter.widget.attrs.update(
        {'class': 'form-select', 'id': 'id_second_reiter', 'name': 'second_reiter', 'required': False})
    class Meta:
        model = Reporting
        fields = ['task_report', 'student_uuid', 'exam_record', 'examiner', 'ers', 'ers_time_start', 'ers_time_end',
                  'first_reiter', 'first_rss_time_start', 'first_rss_time_end', 'rrs_first', 'second_reiter',
                  'second_rss_time_start', 'second_rss_time_end', 'rrs_second', 'completed']


class TaskReportUpdateForm(forms.ModelForm):
    # task_report = forms.ModelChoiceField(queryset=Task.objects.all())
    # task_report.widget.attrs.update(
    #     {'class': 'form-select', 'id': 'id_task_report', 'name': 'task_report', })
    examiner = forms.ModelChoiceField(queryset=CustomUser.objects.filter(is_active=True), required=False)
    examiner.widget.attrs.update(
        {'class': 'form-select', 'id': 'id_examiner', 'name': 'examiner', 'required': False})
    first_reiter = forms.ModelChoiceField(queryset=CustomUser.objects.filter(is_active=True), required=False)
    first_reiter.widget.attrs.update(
        {'class': 'form-select', 'id': 'id_second_reiter', 'name': 'first_reiter', 'required': False})
    second_reiter = forms.ModelChoiceField(queryset=CustomUser.objects.filter(is_active=True), required=False)
    second_reiter.widget.attrs.update(
        {'class': 'form-select', 'id': 'id_second_reiter', 'name': 'second_reiter', 'required': False})

    class Meta:
        model = Reporting
        fields = ['student_uuid', 'exam_record', 'examiner', 'ers', 'ers_time_start', 'ers_time_end',
                  'first_reiter', 'first_rss_time_start', 'first_rss_time_end', 'rrs_first', 'second_reiter',
                  'second_rss_time_start', 'second_rss_time_end', 'rrs_second', 'completed']

