from django.urls import path
import authapp.views as auth_views

app_name = 'authapp'

urlpatterns = [
    path('', auth_views.main, name='main'),
    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, name='logout'),
    path('register/', auth_views.register, name='register'),
    path('forgot/', auth_views.forgot, name='forgot'),
    path('terms/', auth_views.terms, name='terms'),
    path('users/', auth_views.UsersList.as_view(), name='list_users'),
    path('bugreport/', auth_views.BugReportList.as_view(), name='bugreport_list'),
    path('bugreport/add/', auth_views.BugReportAdd.as_view(), name='bugreport_add'),
    path('bugreport/<int:pk>/', auth_views.BugReportUpdate.as_view(), name='bugreport_update'),

]
