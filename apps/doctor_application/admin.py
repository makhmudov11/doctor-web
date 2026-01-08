from django.contrib import admin

from apps.doctor_application.models import DoctorApplication


@admin.register(DoctorApplication)
class DoctorApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'region', 'district', 'address', 'full_name', 'birth_date', 'gender',
                 'experience_year', 'bio', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'gender', 'experience_year']
    search_fields = ['region', 'district', 'full_name', 'bio']