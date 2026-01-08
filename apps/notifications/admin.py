from django.contrib import admin

from apps.notifications.models import FCMDevice


# Register your models here.

@admin.register(FCMDevice)
class AdminFCMDevice(admin.ModelAdmin):
    list_display = ['id', 'user', 'token', 'is_active']