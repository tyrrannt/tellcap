import datetime
import os
import pathlib

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from authapp.models import CustomUser
from tasks.forms import PurposeAddForm, PurposeUpdateForm, FileUploadAddForm, FileUploadDeleteForm, FileUploadUpdateForm
from tasks.models import Task, Reporting, FileUpload
from tellcap.settings import BASE_DIR
from tests.views import get_category


# Create your views here.
class PurposeList(LoginRequiredMixin, ListView):
    model = Task
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        examiner_list = CustomUser.objects.filter(organisation=self.request.user.organisation)
        if self.request.user.is_superuser:
            qs = Task.objects.filter(visible_date_end__gte=datetime.datetime.now(tz=timezone.utc)).filter(
                deleted=False).order_by('pk').reverse()
        elif self.request.user.superintendent:
            qs = Task.objects.filter(examiner__in=examiner_list).filter(
                visible_date_end__gte=datetime.datetime.now(tz=timezone.utc)).filter(deleted=False).order_by(
                'pk').reverse()
        else:
            qs = Task.objects.filter(examiner=self.request.user).filter(
                visible_date_end__gte=datetime.datetime.now(tz=timezone.utc)).filter(deleted=False).order_by(
                'pk').reverse()
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f':: TELLCAP :: Задачи'
        context['category'] = get_category()
        return context


class PurposeAdd(LoginRequiredMixin, CreateView):
    model = Task
    form_class = PurposeAddForm

    def get_context_data(self, **kwargs):
        context = super(PurposeAdd, self).get_context_data(**kwargs)
        if not self.request.user.is_superuser:
            context['form'].fields['examiner'].queryset = CustomUser.objects.filter(
                organisation=self.request.user.organisation)
        return context

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f':: TELLCAP :: Создание задачи'
        context['category'] = get_category()
        return context


class PurposeUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = PurposeUpdateForm

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     obj = self.get_object(qs)
    #     print(obj)
    #     obj_item = Reporting.objects.filter(task_report_id=obj)
    #     print(obj_item)
    #     if obj.reporting:
    #         print('yes')
    #     else:
    #         print('no')
    #     return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f':: TELLCAP :: Редактирование задачи'
        context['category'] = get_category()
        return context

    def get(self, request, *args, **kwargs):
        result = request.GET.get('delete', None)
        if result == '0':
            delete_object = self.get_object()
            delete_object.deleted = True
            delete_object.save()
        if result == '1':
            delete_object = self.get_object()
            delete_object.deleted = False
            delete_object.save()
        # sort_item = request.GET.get('sort_item', None)
        # if sort_item:
        #     self.request.session['sort_item'] = sort_item
        # if result:
        #     self.request.session['portal_paginator'] = result

        return super(PurposeUpdate, self).get(self, request, *args, **kwargs)


class FileUploadList(LoginRequiredMixin, ListView):
    model = FileUpload
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().order_by('pk')
        return qs


class FileUploadUpdate(LoginRequiredMixin, UpdateView):
    model = FileUpload
    form_class = FileUploadUpdateForm

    def form_valid(self, form):
        if form.is_valid():
            obj_item = self.get_object()
            path = pathlib.Path.joinpath(BASE_DIR, 'media', obj_item.file_field.name)
            os.remove(path)
        return super().form_valid(form)


class FileUploadAdd(LoginRequiredMixin, CreateView):
    model = FileUpload
    form_class = FileUploadAddForm

    def form_valid(self, form):
        if self.request.POST:
            file_item = self.request.FILES['file_field'].name
            obj_item = FileUpload.objects.filter(file_field=file_item)
            obj_pk = obj_item.first()
            errors = {'Файл': 'Уже загружен'}
            if obj_item.count() > 0:
                form.add_error('file_field', forms.ValidationError(f'Уже загружен. <a href="/tasks/upload/{obj_pk.pk}" class="btn btn-primary">Заменить?</a>'))

                return self.form_invalid(form)
        return super().form_valid(form)


class FileUploadDelete(LoginRequiredMixin, DeleteView):
    model = FileUpload
    success_url = reverse_lazy('tasks:file_list')
