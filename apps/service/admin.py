from django.contrib import admin

from apps.service.models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    search_fields = ['name', 'description', 'id',]
    list_filter = ['name', 'status']