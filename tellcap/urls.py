"""tellcap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
import tests.views as tests_views
from django.http import HttpResponse


handler404 = tests_views.show_404

def read_file(request):
    f = open('.well-known/pki-validation/E9FC8C4F448C036D654B2DDE18DA1A94.txt', 'r')
    file_content = f.read()
    f.close()
    return HttpResponse(file_content, content_type="text/plain")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', tests_views.main, name='main'),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('tests/', include('tests.urls', namespace='tests')),
    path('tasks/', include('tasks.urls', namespace='tasks')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('.well-known/pki-validation/E9FC8C4F448C036D654B2DDE18DA1A94.txt', read_file),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

