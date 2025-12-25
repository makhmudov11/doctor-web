"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.profile, name='profile')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='profile')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include

import config.settings
from apps.utils.swagger.swagger_urls import SPECTACULAR_URL

def home(request):
    return HttpResponse("Salom, bu mening asosiy sahifam!")

urlpatterns = [
    path('super-admin/', admin.site.urls),
    path('admin/', include('apps.admin.urls', namespace='custom_admin')),
    path('users/', include('apps.users.urls', namespace='users')),
    path('', home, name='home'),
    path('profile/', include('apps.profile.urls', namespace='profile')),

] + SPECTACULAR_URL

if config.settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


