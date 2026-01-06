from django.contrib import admin

from apps.banner.models import Banner


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'url', 'status', '_type', 'image', ]
    search_fields = ['title', 'description', 'id', 'status']
    list_filter = ['status', '_type']
