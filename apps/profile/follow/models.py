from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models

from apps.profile.choices import FollowChoices
from apps.profile.doctor.models import DoctorProfile
from apps.profile.patient.models import PatientProfile
from apps.users.choices import CustomUserRoleChoices
from apps.utils.base_models import CreateUpdateBaseModel

User = get_user_model()


class Follow(CreateUpdateBaseModel):
    profile_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='followings')
    profile_obj_id = models.PositiveIntegerField()
    profile = GenericForeignKey('profile_content_type', 'profile_obj_id')
    following = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='followers')
    status = models.CharField(max_length=50, null=True,
                              default=FollowChoices.FOLLOW,
                              choices=FollowChoices.choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'profile_content_type',
                    'profile_obj_id',
                    'following',
                ],
                name='unique_follow'
            )
        ]
        db_table = 'follow'
        verbose_name = 'Follow'
        verbose_name_plural = 'Follows'

    def clean(self):
        if self.following.user.active_role != CustomUserRoleChoices.SHIFOKOR:
            raise ValidationError("Faqat shifokorlaga obuna bo'lish mumkin")

    @staticmethod
    def get_follow_count(profile):
        return Follow.objects.filter(
            profile_content_type=ContentType.objects.get_for_model(profile),
            profile_obj_id=profile.id,
            status=FollowChoices.FOLLOW
        ).count()

    @staticmethod
    def get_follower_count(profile):
        return Follow.objects.filter(
            following=profile,
            status=FollowChoices.FOLLOW
        ).count()

    def __str__(self):
        return f"{self.profile.full_name} --> {self.following.full_name}"
