from django.urls import path
import tests.views as tests_views

app_name = 'tests'

urlpatterns = [
    path('', tests_views.main, name='main'),
    path('categories/', tests_views.CategoryList.as_view(), name='list_category'),
    path('categories/add/', tests_views.CategoryAdd.as_view(), name='add_category'),
    path('categories/delete/<int:pk>/', tests_views.CategoryDelete.as_view(), name='delete_category'),
    path('categories/<int:pk>/', tests_views.CategoryView.as_view(), name='view_category'),
    path('categories/edit/<int:pk>/', tests_views.CategoryEdit.as_view(), name='edit_category'),
    path('tests/', tests_views.TestList.as_view(), name='list_tests'),
    path('test/add/', tests_views.TestAdd.as_view(), name='add_test'),
    path('test/delete/<int:pk>/', tests_views.TestDelete.as_view(), name='delete_test'),
    path('test/<int:pk>/', tests_views.TestView.as_view(), name='view_test'),
    path('test/edit/<int:pk>/', tests_views.TestEdit.as_view(), name='edit_test'),
    path('category/<int:pk>/', tests_views.category, name='category'),
    path('testing/<int:pk>/', tests_views.testing, name='testing'),
    path('reporting/', tests_views.TaskReportsList.as_view(), name='task_reports'),
    path('reporting/add/', tests_views.TaskReportsAdd.as_view(), name='task_report_add'),
    path('reporting/<int:pk>/', tests_views.TaskReportsEdit.as_view(), name='task_report_edit'),
]
