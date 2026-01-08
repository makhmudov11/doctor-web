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


def home(request):
    return HttpResponse("Home page")


from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

import config.settings
from apps.utils.swagger.swagger_urls import SPECTACULAR_URL

TOKEN_REFRESH = [
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]

urlpatterns = [
                  path('', home, name='home'),
                  path('admin/', admin.site.urls),
                  path('super-admin/', include('apps.super_admin.urls', namespace='super_admin')),
                  path('users/', include('apps.users.urls', namespace='users')),
                  path('doctor_application/', include('apps.doctor_application.urls', namespace='doctor_application')),
                  path('notifications/', include('apps.notifications.urls', namespace='notifications')),
                  path('banner/', include('apps.banner.urls', namespace='banner')),
                  path('service/', include('apps.service.urls', namespace='service')),
                  path('profile/', include('apps.profile.urls', namespace='profile')),
                  path('content/', include('apps.video.urls', namespace='content')),
                  path('history/', include('apps.history.urls', namespace='history')),
                  path('order/', include('apps.order.urls', namespace='order')),

              ] + SPECTACULAR_URL + TOKEN_REFRESH

if config.settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
