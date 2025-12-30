from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.profile.models import PatientProfile
from apps.users.choices import CustomUserRoleChoices
from apps.users.models import CustomUser


@receiver(post_save, sender=CustomUser)
def create_patient_profile_after_created_user(sender, instance, created, **kwargs):
    if created and instance.active_role == CustomUserRoleChoices.BEMOR:
        PatientProfile.objects.create(user=instance)