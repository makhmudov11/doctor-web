from django.urls import path

from apps.notifications.views import FCMDeviceCreateAPIView, FCMDeviceLogoutAPIView

app_name = 'notifications'

urlpatterns = [
    path('device/create/', FCMDeviceCreateAPIView.as_view(), name='device-create'),
    path('device/logout/', FCMDeviceLogoutAPIView.as_view(), name='device-logout')
]