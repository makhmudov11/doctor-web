from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DoctorApplication, DoctorApplicationChoices
from ..users.choices import CustomUserRoleChoices


@receiver(post_save, sender=DoctorApplication)
def add_doctor_role(sender, instance, created, **kwargs):
    if not created and instance.status == DoctorApplicationChoices.APPROVED:
        user = instance.user
        if not isinstance(user.roles, list):
            user.roles = []
        if CustomUserRoleChoices.SHIFOKOR not in user.roles:
            user.roles.append(CustomUserRoleChoices.SHIFOKOR)
            user.save()
