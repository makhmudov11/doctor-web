from django.urls import path, include

app_name = 'super_admin'

urlpatterns = [
    path('users/', include('apps.super_admin.urls.users')),
    path('users/profile/', include('apps.super_admin.urls.profile'))
]