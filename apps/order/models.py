from django.db import models

from apps.profile.models import PatientProfile
from apps.utils.base_models import CreateUpdateBaseModel, GenderChoices


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



