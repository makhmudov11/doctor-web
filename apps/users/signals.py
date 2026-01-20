from datetime import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.order.models import AddPatient
from apps.profile.models import PatientProfile
from apps.transactions.models import UserUniqueBalanceID
from apps.users.choices import CustomUserRoleChoices
from apps.users.models import CustomUser
from apps.utils.base_models import GenderChoices


@receiver(post_save, sender=CustomUser)
def create_patient_profile_after_user_verified(sender, instance, created, **kwargs):
    if not created and instance.active_role == CustomUserRoleChoices.BEMOR and instance.is_active:
        profile = getattr(instance, 'patient_profile', None)
        if not profile:
            profile = PatientProfile.objects.create(user=instance)

        birth_date = instance.birth_date or datetime.strptime('01.01.2001', '%d.%m.%Y').date()
        AddPatient.objects.create(
            patient=profile,
            full_name=instance.full_name or '',
            gender=instance.gender or GenderChoices.ERKAK,
            birth_date=birth_date,
            is_self=True
        )

        UserUniqueBalanceID.objects.get_or_create(user=instance)
