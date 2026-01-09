from django.urls import path

from apps.notifications.views import FCMDeviceCreateAPIView, FCMDeviceLogoutAPIView, NotificationReadAPIView, \
    NotificationDeleteAPIView, NotificationListAPIView, NotificationDetailAPIView

app_name = 'notifications'

urlpatterns = [
    path('device/create/', FCMDeviceCreateAPIView.as_view(), name='device-create'),
    path('device/logout/', FCMDeviceLogoutAPIView.as_view(), name='device-logout'),
    path('read/<int:notification_id>/', NotificationReadAPIView.as_view(), name='notif-read'),
    path('delete/<int:notification_id>/', NotificationDeleteAPIView.as_view(), name='notif-delete'),
    path('detail/<int:notification_id>/', NotificationDetailAPIView.as_view(), name='notif-detail'),
    path('list/', NotificationListAPIView.as_view(), name='notif-list'),
]