from django.urls import path
import tasks.views as tasks_views

app_name = 'tasks'

urlpatterns = [
    # path('', tasks_views.main, name='main'),
    path('purpose/', tasks_views.PurposeList.as_view(), name='purpose_list'),
    path('purpose/add/', tasks_views.PurposeAdd.as_view(), name='purpose_add'),
    path('purpose/<int:pk>/', tasks_views.PurposeUpdate.as_view(), name='purpose_update'),
    path('upload/', tasks_views.FileUploadList.as_view(), name='file_list'),
    path('upload/add/', tasks_views.FileUploadAdd.as_view(), name='file_add'),
    path('upload/delete/<int:pk>/', tasks_views.FileUploadDelete.as_view(), name='file_delete'),
    path('upload/<int:pk>/', tasks_views.FileUploadUpdate.as_view(), name='file_update'),
    ]