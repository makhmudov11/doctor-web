from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DoctorApplication, DoctorApplicationChoices
from ..profile.models import DoctorProfile
from ..users.choices import CustomUserRoleChoices


@receiver(post_save, sender=DoctorApplication)
def add_doctor_role(sender, instance, created, **kwargs):
    if created:
        return

    if instance.status != DoctorApplicationChoices.APPROVED:
        return

    def on_commit():
        user = instance.user

        roles = user.roles or []
        if CustomUserRoleChoices.SHIFOKOR not in roles:
            roles.append(CustomUserRoleChoices.SHIFOKOR)
            user.roles = roles
            user.save(update_fields=["roles"])

        DoctorProfile.objects.update_or_create(
            user=user,
            defaults={
                "specialization": instance.specialization,
                "experience_years": instance.experience_years,
                "bio": instance.bio,
                "service_fee": instance.service_fee
            }
        )

    transaction.on_commit(on_commit)
