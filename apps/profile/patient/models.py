from django.contrib.auth import get_user, get_user_model
from django.db import models
from django.utils.text import slugify

from apps.utils.base_models import CreateUpdateBaseModel
from apps.utils.generate_code import generate_public_id, generate_code

User = get_user_model()


class PatientProfile(CreateUpdateBaseModel):
    public_id = models.PositiveBigIntegerField(unique=True, db_index=True, default=generate_code)
    user = models.OneToOneField(User,
                                on_delete=models.SET_NULL,
                                null=True,
                                related_name='patient_profile'
                                )
    following_count = models.PositiveIntegerField(default=0)
    slug = models.CharField(null=True, blank=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'patient_profile'
        verbose_name = 'Patient Profile'
        verbose_name_plural = 'Patients Profile'

    def __str__(self):
        return self.user.full_name or self.user.contact or self.public_id

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.full_name)
        if not self.public_id:
            self.public_id = generate_public_id(PatientProfile)
        super().save(*args, **kwargs)
