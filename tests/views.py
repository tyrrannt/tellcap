from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.utils import timezone

from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
import datetime
from django.db.models import Q
from django.core.paginator import Paginator

from authapp.models import CustomUser
# Create your views here.
from tasks.models import Task, Reporting
from tests.models import Category, Test
from re import sub as replace_mp3
from tests.forms import TaskReportAddForm, TaskReportUpdateForm


def show_404(request, exception=None):
    return render(request, 'tests/404.html')


def get_category():
    return Category.objects.all()


"""
Главная страница сайта
"""


@login_required
def main(request, pk=None):
    title = ':: TELLCAP :: Главная'
    categoryes = Category.objects.all()
    if request.user.is_staff:
        tests = Test.objects.all()
    else:
        tasks1 = Task.objects.filter(examiner=request.user).filter(
            Q(visible_date_start__lte=datetime.datetime.now(tz=timezone.utc)),
            Q(visible_date_end__gte=datetime.datetime.now(tz=timezone.utc)))
        tasks2 = Task.objects.filter(Q(examiner__username='admin'))
        tests = tasks1 | tasks2
    content = {'title': title, 'category': categoryes, 'test': tests}
    paginator = Paginator(tests.order_by('id'), 6)
    if request.user.is_staff:
        paginator = Paginator(tests.order_by('name'), 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    content = {'title': title, 'category': categoryes, 'page_obj': page_obj, 'date_time': timezone.localtime(timezone.now())}
    request.session.set_expiry(900)
    request.session['purpose_expire'] = '0'
    return render(request, 'tests/index.html', content)


@login_required
def category(request, pk=None):
    categoryes = Category.objects.all()
    try:
        title = ':: TELLCAP :: ' + categoryes.get(pk=pk).name
    except Exception as ex:
        raise Http404
    tests = Test.objects.filter(category=categoryes.get(pk=pk))
    paginator = Paginator(tests.order_by('name'), 6)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    content = {'title': title, 'category': categoryes, 'page_obj': page_obj, }
    request.session.set_expiry(900)
    return render(request, 'tests/index.html', content)


"""
Вывод страницы теста
"""


@login_required
def testing(request, pk=None):
    title = ':: TELLCAP :: Главная'
    categoryes = Category.objects.all()

    if request.user.is_superuser:
        tests = get_object_or_404(Test, pk=pk)
    else:
        try:
            tests = get_object_or_404(Test, pk=pk)
            tasks1 = Task.objects.filter(examiner__pk=request.user.pk).filter(
                Q(visible_date_start__lte=datetime.datetime.utcnow()),
                Q(visible_date_end__gte=datetime.datetime.utcnow()))
            tasks2 = Task.objects.filter(Q(examiner__username='admin'))
            tasks = tasks1 | tasks2
            if not tasks.filter(test_module__pk=tests.pk).exists():
                raise Http404
        except Exception as ex:
            raise Http404

    desc_mp3 = tests.description
    tests.description = replace_mp3(r'<.*>(.*\.mp3)</.*>', r'<audio controls="controls" crossorigin="anonymous" '
                                                           r'style="width:100%;" controlsList="nodownload"><source src="/media/\1" '
                                                           r'type="audio/mpeg"></audio>', desc_mp3)
    desc_wav = tests.description
    tests.description = replace_mp3(r'<.*>(.*\.wav)</.*>', r'<audio controls="controls" crossorigin="anonymous" '
                                                           r'style="width:100%;" controlsList="nodownload"><source src="/media/\1" '
                                                           r'type="audio/mpeg"></audio>', desc_wav)
    content = {'title': title, 'category': categoryes, 'tests': tests}
    request.session.set_expiry(900)
    return render(request, 'tests/tests.html', content)


"""
Вывод списка категорий
"""


class CategoryList(LoginRequiredMixin, ListView):
    model = Category

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ':: TELLCAP :: Список категорий'
        context['category'] = get_category()
        return context


"""
Добавление новой категории
"""


class CategoryAdd(LoginRequiredMixin, CreateView):
    # form_class = CategoryForm
    model = Category
    # template_name = 'tests/category_form.html'
    fields = ['name', 'description', 'is_active']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ':: TELLCAP :: Добавление категории'
        context['category'] = get_category()
        return context


"""
Просмотр отдельной категории
"""


class CategoryView(LoginRequiredMixin, DetailView):
    model = Category

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ':: TELLCAP :: Просмотр категории'
        context['category'] = get_category()
        return context


"""
Редактирование отдельной категории
"""


class CategoryEdit(LoginRequiredMixin, UpdateView):
    model = Category
    fields = ['name', 'description', 'is_active']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ':: TELLCAP :: Редактирование категории'
        context['category'] = get_category()
        return context


class CategoryDelete(LoginRequiredMixin, DeleteView):
    model = Category
    # template_name = 'post_delete.html'
    success_url = reverse_lazy('tests:list_category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ':: TELLCAP :: Удаление категории'
        context['category'] = get_category()
        return context


class TestList(LoginRequiredMixin, ListView):
    model = Test
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ':: TELLCAP :: Список тестов'
        context['category'] = get_category()
        return context

    def get_queryset(self):
        query_set = self.model.objects.order_by('name')
        return query_set


class TestAdd(LoginRequiredMixin, CreateView):
    # form_class = TestForm
    model = Test
    # template_name = 'tests/category_form_add.html'
    fields = ['category', 'name', 'description', 'is_active', 'author', 'created']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ':: TELLCAP :: Добавление теста'
        context['category'] = get_category()
        return context


class TestView(LoginRequiredMixin, DetailView):
    model = Test

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ':: TELLCAP :: Просмотр теста'
        context['category'] = get_category()
        return context


class TestEdit(LoginRequiredMixin, UpdateView):
    model = Test
    fields = ['category', 'name', 'description', 'is_active', 'author', 'created']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ':: TELLCAP :: Редактирование категории'
        context['category'] = get_category()
        return context


class TestDelete(LoginRequiredMixin, DeleteView):
    model = Test
    # template_name = 'post_delete.html'
    success_url = reverse_lazy('tests:list_tests')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ':: TELLCAP :: Удаление теста'
        context['category'] = get_category()
        return context


class TaskReportsList(LoginRequiredMixin, ListView):
    model = Reporting
    paginate_by = 10

    def get_queryset(self):
        examiner_list = CustomUser.objects.filter(organisation=self.request.user.organisation)
        if self.request.user.is_superuser:
            qs = Reporting.objects.all().order_by('pk').reverse()
        elif self.request.user.superintendent:
            qs = Reporting.objects.filter(examiner__in=examiner_list).order_by('pk').reverse()
        else:
            qs = Reporting.objects.filter(reporting_visible=True).filter(
                Q(examiner=self.request.user) | Q(first_reiter=self.request.user) | Q(
                    second_reiter=self.request.user)).order_by('pk').reverse()
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f':: TELLCAP :: Отчеты'
        context['category'] = get_category()
        return context


class TaskReportsAdd(LoginRequiredMixin, CreateView):
    model = Reporting
    form_class = TaskReportAddForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f':: TELLCAP :: Добавление отчета'
        context['category'] = get_category()
        return context


class TaskReportsEdit(LoginRequiredMixin, UpdateView):
    model = Reporting
    form_class = TaskReportUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        test_module = self.object.task_report.test_module.name
        test_module_name = self.object.task_report
        description = ""
        now = datetime.datetime.utcnow()
        today = datetime.date(now.year, now.month, now.day)
        try:
            # Проверка доступности теста exp_ = истина (не доступен) иначе (доступен)
            context['exp_examiner'] = True if self.object.ers_time_end < today else False
            # Также проверка доступности материала для рейтирования, если время прошло, доступ закрывается
            if self.object.ers_time_end > today and self.request.user == self.object.examiner:
                description = Test.objects.get(name__contains=(test_module[:-1] + 'R'))
        except TypeError:
            pass
        try:
            # Проверка доступности теста exp_ = истина (не доступен) иначе (доступен)
            context['exp_reiter1'] = True if self.object.first_rss_time_end < today else False
            # Также проверка доступности материала для рейтирования, если время прошло, доступ закрывается
            if self.object.first_rss_time_end > today and self.request.user == self.object.first_reiter:
                description = Test.objects.get(name__contains=(test_module[:-1] + 'R'))
        except TypeError:
            pass
        try:
            # Проверка доступности теста exp_ = истина (не доступен) иначе (доступен)
            context['exp_reiter2'] = True if self.object.second_rss_time_end < today else False
            # Также проверка доступности материала для рейтирования, если время прошло, доступ закрывается
            if self.object.second_rss_time_end > today and self.request.user == self.object.second_reiter:
                description = Test.objects.get(name__contains=(test_module[:-1] + 'R'))
        except TypeError:
            pass
        if not self.request.user.is_superuser:
            context['form'].fields['examiner'].queryset = CustomUser.objects.filter(
                organisation=self.request.user.organisation)
            context['form'].fields['first_reiter'].queryset = CustomUser.objects.filter(
                organisation=self.request.user.organisation)
            context['form'].fields['second_reiter'].queryset = CustomUser.objects.filter(
                organisation=self.request.user.organisation)
        context['description'] = description
        context['test_module'] = test_module_name
        context['title'] = f':: TELLCAP :: Отчет {test_module_name}'
        context['category'] = get_category()
        return context
