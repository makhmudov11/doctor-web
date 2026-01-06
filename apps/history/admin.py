from django.contrib import admin

from apps.history.models import Address


# Register your models here.
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient','district','region','street',
                    'longitude','latitude','home','building_number', 'entrance', 'status', 'created_at']