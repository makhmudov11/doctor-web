from django.contrib.auth import get_user_model
from django.db import models

from apps.utils.base_models import CreateUpdateBaseModel, GenderChoices

User = get_user_model()


class DoctorApplicationChoices(models.TextChoices):
    PENDING = 'pending' 'Pending'
    APPROVED = 'approved' 'Approved'
    CANCELLED = 'cancelled' 'Cancelled'
    FINISHED = 'finished' 'Finished'


class DoctorApplication(CreateUpdateBaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='doctor_applications')
    image = models.ImageField(upload_to='doctor_application/doctor_image/', )
    region = models.CharField(max_length=200, db_index=True)
    district = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    full_name = models.CharField(max_length=200, db_index=True)
    birth_date = models.DateField()
    gender = models.CharField(choices=GenderChoices.choices)
    passport = models.CharField(max_length=20)
    passport_image = models.ImageField(upload_to='doctor_application/passport_image/')
    passport_image2 = models.ImageField(upload_to='doctor_application/passport_image2/')
    diplom_image = models.ImageField(upload_to='doctor_application/diplom_image/')
    bio = models.TextField()
    experience_year = models.PositiveSmallIntegerField()
    specialization = models.CharField(max_length=100)
    term = models.DateTimeField(null=True)
    status = models.CharField(max_length=50, choices=DoctorApplicationChoices.choices,
                              default=DoctorApplicationChoices.PENDING)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'doctor_application'
        verbose_name = 'Doctor Application'
        verbose_name_plural = 'Doctor Applications'
        ordering = ['created_at']
