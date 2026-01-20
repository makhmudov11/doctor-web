from django.contrib import admin

from apps.order.models import AddPatient, MedicalService
from .models import Order, OrderDetail, OrderDetailImage


# Register your models here.
@admin.register(AddPatient)
class AddPatientAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'full_name', 'gender', 'birth_date']


@admin.register(MedicalService)
class MedicalServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'status', 'package_code', 'code', 'units']


class OrderDetailInline(admin.TabularInline):
    model = OrderDetail
    extra = 0


class OrderDetailImageInline(admin.TabularInline):
    model = OrderDetailImage
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_id',
        'patient',
        'add_patient',
        'doctor',
        'payment_type',
        'status',
        'summa',
        'created_at',
    )
    list_filter = ('status', 'payment_type', 'created_at')
    search_fields = ('order_id', 'patient__full_name', 'doctor__full_name')
    ordering = ('-created_at',)
    readonly_fields = ('order_id', 'created_at', 'updated_at')
    inlines = [OrderDetailInline, OrderDetailImageInline]


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'created_at')
    search_fields = ('order__order_id',)
    list_filter = ('created_at',)


@admin.register(OrderDetailImage)
class OrderDetailImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'prescription', 'created_at')
    search_fields = ('order__order_id',)
    list_filter = ('created_at',)
