from django.contrib import admin

from apps.service.models import Service, SocialNetwork


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'image']
    search_fields = ['name', 'description', 'id',]
    list_filter = ['name', 'status']

@admin.register(SocialNetwork)
class SocialNetworkAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'image', 'link', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['id', 'title', 'description', 'image', 'link', 'status', 'created_at']