from django.urls import path, include

from apps.super_admin.views.users import AdminLoginAPIView

app_name = 'super_admin'

urlpatterns = [
    path('login/', AdminLoginAPIView.as_view(), name='admin-login'),
    path('users/', include('apps.super_admin.urls.users')),
    path('users/profile/', include('apps.super_admin.urls.profile')),
    path('home/', include('apps.super_admin.urls.services'))
]