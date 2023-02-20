from django import forms

from authapp.models import CustomUser
from tasks.models import Task, FileUpload
from tests.models import Test


class PurposeAddForm(forms.ModelForm):
    test_module = forms.ModelChoiceField(queryset=Test.objects.all())
    test_module.widget.attrs.update(
        {'class': 'form-select', 'id': 'id_test_module', 'name': 'test_module'})
    examiner = forms.ModelChoiceField(queryset=CustomUser.objects.filter(is_active=True))
    examiner.widget.attrs.update(
        {'class': 'form-select', 'id': 'id_examiner', 'name': 'examiner'})
    class Meta:
        model = Task
        fields = ['test_module', 'examiner', 'student_uuid', 'visible_date_start', 'visible_date_end', 'create_reporting']


class PurposeUpdateForm(forms.ModelForm):
    test_module = forms.ModelChoiceField(queryset=Test.objects.all())
    test_module.widget.attrs.update(
        {'class': 'form-select', 'id': 'id_test_module', 'name': 'test_module'})
    examiner = forms.ModelChoiceField(queryset=CustomUser.objects.filter(is_active=True))
    examiner.widget.attrs.update(
        {'class': 'form-select', 'id': 'id_examiner', 'name': 'examiner'})
    visible_date_start = forms.DateTimeField(input_formats='%Y-%m-%d %H:%M')
    visible_date_end = forms.DateTimeField(input_formats='%Y-%m-%d %H:%M')
    class Meta:
        model = Task
        fields = ['test_module', 'examiner', 'visible_date_start', 'visible_date_end', 'create_reporting', 'student_uuid', 'deleted']


class FileUploadAddForm(forms.ModelForm):
    file_field = forms.FileField()

    class Meta:
        model = FileUpload
        fields = ['file_field']


class FileUploadUpdateForm(forms.ModelForm):
    file_field = forms.FileField()

    class Meta:
        model = FileUpload
        fields = ['file_field']

class FileUploadDeleteForm(forms.ModelForm):
    file_field = forms.FileField()

    class Meta:
        model = FileUpload
        fields = ['file_field']