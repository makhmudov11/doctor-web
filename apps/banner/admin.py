from django.contrib import admin

from apps.banner.models import Banner


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'title', 'description', 'url', 'status', '_type']
    search_fields = ['title', 'description', 'id', 'status']
    list_filter = ['status', '_type']