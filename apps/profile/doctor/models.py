from django.contrib.auth import get_user_model
from django.db import models
from rest_framework.exceptions import ValidationError
from apps.users.choices import CustomUserRoleChoices
from apps.utils.base_models import CreateUpdateBaseModel
from apps.utils.generate_code import generate_public_id, generate_code

User = get_user_model()


class DoctorProfile(CreateUpdateBaseModel):
    public_id = models.PositiveBigIntegerField(unique=True, default=generate_code)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name='doctor_profile')
    username = models.CharField(max_length=200, null=True, unique=True, db_index=True)
    specialization = models.CharField(max_length=255, null=True)
    experience_years = models.PositiveSmallIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)
    followers_count = models.PositiveIntegerField(default=0)
    posts_count = models.PositiveSmallIntegerField(default=0)
    is_private = models.BooleanField(default=False)

    class Meta:
        db_table = 'doctor_profile'
        verbose_name = 'Doctor Profile'
        verbose_name_plural = 'Doctors Profile'
        ordering = ['-created_at']

    def __str__(self):
        return self.user.full_name or self.username or self.base.public_id

    def clean(self):
        if self.user.active_role != CustomUserRoleChoices.SHIFOKOR:
            raise ValidationError("Role doctor bo'lishi kerak")

    def save(self, *args, **kwargs):
        if not self.public_id:
            self.public_id = generate_public_id(DoctorProfile)
        self.full_clean()
        super().save(*args, **kwargs)
