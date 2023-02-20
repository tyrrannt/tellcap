from django.contrib.auth.forms import AuthenticationForm
from django import forms

from authapp.models import BugReport, CustomUser


class UserLoginForm(AuthenticationForm):
    class Meta:
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['password'].widget.attrs['placeholder'] = 'Введите пароль'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-2'


class BugReportAddForm(forms.ModelForm):
    # bug_report_user = forms.ModelChoiceField(queryset=CustomUser.objects.all(), required=False)
    # bug_report_user.widget.attrs.update(
    #     {'class': 'form-select', 'id': 'id_bug_report_user', 'name': 'bug_report_user', 'required': False})
    # bug_report_user.widget.attrs.update(
    #     {'class': 'form-select', 'id': 'id_bug_report_user', 'name': 'bug_report_user', })
    class Meta:
        model = BugReport
        fields = ('bug_report_user', 'subject', 'description')



class BugReportUpdateForm(forms.ModelForm):
    class Meta:
        model = BugReport
        fields = ('bug_report_user', 'subject', 'description')