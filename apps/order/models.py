from django.db import models

from apps.history.models import Address
from apps.profile.models import PatientProfile, DoctorProfile
from apps.utils.base_models import CreateUpdateBaseModel, GenderChoices
from django.utils.translation import gettext_lazy as _

from apps.utils.generate_code import generate_unique_order_id


class AddPatient(CreateUpdateBaseModel):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='add_patients')
    full_name = models.CharField(max_length=200, null=True)
    birth_date = models.DateField(null=True)
    image = models.ImageField(upload_to='add_patient/', null=True, blank=True)
    gender = models.CharField(choices=GenderChoices.choices, default=GenderChoices.ERKAK)
    is_self = models.BooleanField(default=False)

    class Meta:
        db_table = 'add_patient'
        verbose_name = 'Add Patient'
        verbose_name_plural = 'Add Patients'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.patient.user.full_name or self.patient.public_id} --> {self.full_name}"


class MedicalService(CreateUpdateBaseModel):
    name = models.TextField(null=True, verbose_name=_("Mahsulot nomi"))
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name=_("Narxi"))
    units = models.PositiveIntegerField(null=True)
    code = models.CharField(max_length=100, null=True, verbose_name=_("MXIK kodi"))
    package_code = models.CharField(max_length=100, null=True, verbose_name=_("O'lchov birligi"))
    vat_percent = models.PositiveSmallIntegerField(null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ----- {self.price}"

    class Meta:
        db_table = 'medical_services'
        verbose_name = 'Medical Service'
        verbose_name_plural = 'Medical Services'
        ordering = ['created_at']


class OrderStatusChoices(models.TextChoices):
    WAITING = _('waiting'), 'Kutilmoqda'
    ACCEPTED = _('accepted'), 'Qabul qilindi'
    ON_THE_WAY = _('on the way'), 'Yetib kelmoqda'
    ARRIVED = _('arrived'), 'Yetib keldi'
    FINISHED = _('finished'), 'Tugallandi'
    CANCELLED = _("cancelled"), "Bekor qilindi"


class PaymentTypeChoice(models.TextChoices):
    BALANS = 'balance', 'User Balance'
    CASH = 'cash', 'Cash Payment'


class Order(CreateUpdateBaseModel):
    order_id = models.CharField(unique=True, max_length=10)
    patient = models.ForeignKey(PatientProfile, on_delete=models.SET_NULL, null=True, related_name='patient_orders')
    add_patient = models.ForeignKey(AddPatient, on_delete=models.SET_NULL, null=True, related_name='add_patient_orders')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True, related_name='doctor_orders')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, related_name='address_orders')
    payment_type = models.CharField(choices=PaymentTypeChoice.choices, default=PaymentTypeChoice.CASH)
    status = models.CharField(max_length=200, choices=OrderStatusChoices.choices, default=OrderStatusChoices.WAITING)
    rating = models.FloatField(default=0, blank=True)
    comment = models.TextField(null=True, blank=True)
    summa = models.PositiveBigIntegerField(default=0, blank=True)

    def __str__(self):
        return f"{self.patient or '-'} ------ {self.doctor or '-'}"

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = generate_unique_order_id()

        super().save(*args, **kwargs)

    class Meta:
        db_table = 'order'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-created_at']


class OrderDetail(CreateUpdateBaseModel):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, related_name='order_details')
    medical_service = models.JSONField(default=list, null=True, blank=True)

    def __str__(self):
        return f"OrderDetail #{self.pk} for Order {self.order.order_id or '-'}"

    class Meta:
        db_table = 'order_detail'
        verbose_name = 'Orders Detail'
        verbose_name_plural = 'Orders Detail'


class OrderDetailImage(CreateUpdateBaseModel):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, related_name='order_images')
    prescription = models.FileField(upload_to='order_image/', null=True, blank=True)

    class Meta:
        db_table = 'order_detail_image'
        verbose_name = 'Orders Detail Image'
        verbose_name_plural = 'Orders Images'

    def __str__(self):
        return f"{self.pk} --- {self.order or '-'} ---- {self.prescription}"
