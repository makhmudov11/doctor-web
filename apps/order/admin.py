from django.contrib import admin

from apps.order.models import AddPatient


# Register your models here.
@admin.register(AddPatient)
class AddPatientAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'full_name', 'gender', 'birth_date']