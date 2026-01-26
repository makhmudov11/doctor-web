from django.contrib import admin

from apps.notifications.models import FCMDevice, Notification


# Register your models here.

@admin.register(FCMDevice)
class AdminFCMDevice(admin.ModelAdmin):
    list_display = ['id', 'user', 'token', 'device_type', 'is_active']
@admin.register(Notification)
class AdminFCMDevice(admin.ModelAdmin):
    list_display = ['id', 'get_device_user_full_name', 'is_read', 'read_at', 'deleted_at', 'message']

    def get_device_user_full_name(self, obj):
        if obj.device and obj.device.user:
            return obj.device.user.full_name
        return "-"

    get_device_user_full_name.short_description = "Foydalanuvchi"