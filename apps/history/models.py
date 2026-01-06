from django.db import models

from apps.profile.models import PatientProfile
from apps.utils.base_models import CreateUpdateBaseModel
from django.utils.translation import gettext_lazy as _


class Address(CreateUpdateBaseModel):
    patient = models.ForeignKey(PatientProfile, on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name=_("Bemor"), related_name='patient_address')
    address_type = models.CharField(max_length=200, null=True, blank=True, verbose_name=_("Manzil turi")) # masalan: ish joy | uy
    district = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Tuman")) # tuman
    region = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Viloyat")) # viloyat | shahar
    street = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Ko'cha")) # kocha
    longitude = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    latitude = models.DecimalField(max_digits=20, decimal_places=5, null=True)
    home = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Uy raqami")) # uy raqami
    building_number = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("Bino raqami")) # dom raqami
    entrance = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Kirish eshik raqami")) # podyezd raqami
    floor = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name=_("Qavat")) # qavat
    notes = models.CharField(null=True, blank=True, max_length=50, verbose_name=_("Izoh")) # komentariya
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.longitude} --- {self.latitude}"

    class Meta:
        db_table = 'address'
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

class Appointment(CreateUpdateBaseModel):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='appointments')
    doctor_name = models.CharField(max_length=255)
    date = models.DateTimeField()
    status = models.CharField(max_length=50)