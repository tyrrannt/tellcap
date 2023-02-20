from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from authapp.forms import UserLoginForm, BugReportAddForm, BugReportUpdateForm
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from authapp.models import CustomUser, BugReport
from tests.models import Category
from tests.views import get_category


def main(request):
    return render(request, 'authapp/index.html')


def login(request):
    title = ':: TELLCAP :: Авторизация'
    if request.method == 'POST':
        login_form = UserLoginForm(data=request.POST)
        if login_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                request.session.set_expiry(3600)
                return HttpResponseRedirect(reverse('tests:main'))
    else:
        login_form = UserLoginForm()
    content = {'title': title, 'login_form': login_form}
    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('authapp:login'))


def register(request):
    title = ':: TELLCAP :: Регистрация'
    content = {'title': title}
    return render(request, 'authapp/register.html', content)


def forgot(request):
    title = ':: TELLCAP :: Восстановление пароля'
    content = {'title': title}
    return render(request, 'authapp/forgot-password.html', content)


def terms(request):
    title = ':: TELLCAP :: Пользовательское соглашение'
    content = {'title': title}
    return render(request, 'authapp/terms.html', content)


class UsersList(LoginRequiredMixin, ListView):
    categoryes = Category.objects.all()
    model = CustomUser

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ':: TELLCAP :: Список пользователей'
        context['category'] = self.categoryes
        return context


class UsersAdd(LoginRequiredMixin, CreateView):
    model = CustomUser


class UsersDetail(LoginRequiredMixin, DetailView):
    model = CustomUser


class UsersUpdate(LoginRequiredMixin, UpdateView):
    model = CustomUser


class BugReportList(LoginRequiredMixin, ListView):
    model = BugReport

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f':: TELLCAP :: Сообщения об ошибках'
        context['category'] = get_category()
        return context


class BugReportAdd(LoginRequiredMixin, CreateView):
    model = BugReport
    form_class = BugReportAddForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f':: TELLCAP :: Создание сообщения об ошибке'
        context['category'] = get_category()
        return context



class BugReportDetail(LoginRequiredMixin, DetailView):
    model = BugReport

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f':: TELLCAP :: Просмотр сообщения об ошибке'
        context['category'] = get_category()
        return context


class BugReportUpdate(LoginRequiredMixin, UpdateView):
    model = BugReport
    form_class = BugReportUpdateForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f':: TELLCAP :: Редактирование сообщения об ошибке'
        context['category'] = get_category()
        return context
