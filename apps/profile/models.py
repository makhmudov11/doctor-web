from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.text import slugify

from apps.profile.choices import FollowChoices, StoryChoices
from apps.users.choices import CustomUserRoleChoices
from apps.utils.base_models import CreateUpdateBaseModel
from django.db import models

from apps.utils.generate_code import generate_public_id
from apps.utils.generate_code import generate_code

User = get_user_model()


class DoctorProfile(CreateUpdateBaseModel):
    public_id = models.PositiveBigIntegerField(unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    username = models.CharField(max_length=200, null=True, unique=True, db_index=True)
    specialization = models.CharField(max_length=255, null=True)
    experience_years = models.PositiveSmallIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)
    followers_count = models.PositiveIntegerField(default=0)
    posts_count = models.PositiveSmallIntegerField(default=0)
    rating = models.FloatField(default=0)
    order_count = models.PositiveIntegerField(default=0)
    is_private = models.BooleanField(default=False)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'doctor_profile'
        verbose_name = 'Doctor Profile'
        verbose_name_plural = 'Doctors Profile'
        ordering = ['-created_at']

    def __str__(self):
        if self.user:
            return self.user.full_name or self.username or self.base.public_id
        return str(self.pk)


    def save(self, *args, **kwargs):
        if not self.public_id:
            self.public_id = generate_public_id(DoctorProfile)
        super().save(*args, **kwargs)


class Follow(CreateUpdateBaseModel):
    profile_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                             related_name='followings')
    profile_obj_id = models.PositiveIntegerField()
    profile = GenericForeignKey('profile_content_type', 'profile_obj_id')
    following = models.ForeignKey('DoctorProfile', on_delete=models.CASCADE, related_name='followers')
    status = models.CharField(max_length=50,
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
        if self.following and self.following.user.active_role != CustomUserRoleChoices.SHIFOKOR:
            raise ValidationError("Faqat shifokorlaga obuna bo'lish mumkin")
        if not self.profile_content_type or self.profile_obj_id:
            print(self.profile_content_type)
            print(self.profile_obj_id)
            raise ValidationError("Bosh qiymat ruxsat etilmagan")
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
        if self.profile and self.following:
            profile_name = self.profile.user.full_name if self.profile.user.full_name else "No Profile Name"
            following_name = self.following.user.full_name if self.following.user.full_name else "No Following Name"
            return f"{profile_name} --> {following_name}"
        return str(self.pk)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class PatientProfile(CreateUpdateBaseModel):
    public_id = models.PositiveBigIntegerField(unique=True, db_index=True, default=generate_code)
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
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


class Story(CreateUpdateBaseModel):
    profile = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE,
                                related_name='story')
    content = models.FileField(upload_to='users/profile/story/')
    content_type = models.CharField(max_length=100,
                                    default=StoryChoices.IMAGE,
                                    choices=StoryChoices.choices)
    view_count = models.PositiveIntegerField(default=0)
    expires_at = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=False)  # is_expired

    def __str__(self):
        return self.profile.user.full_name if self.profile.user else str(self.pk)

    @staticmethod
    def media_type(content):
        content = content.content_type
        if content.startswith('image'):
            content_type = StoryChoices.IMAGE
        elif content.startswith('video'):
            content_type = StoryChoices.VIDEO
        else:
            content_type = None
        return content_type

    def save(self, *args, **kwargs):
        if self.content:
            ext = self.content.name.split('.')[-1].lower()
            if ext in ['mp4', 'mov', 'avi']:
                self.content_type = StoryChoices.VIDEO
            elif ext in ['jpg', 'jpeg', 'png', 'gif']:
                self.content_type = StoryChoices.IMAGE
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at

    class Meta:
        db_table = 'story'
        verbose_name = 'Story'
        verbose_name_plural = 'Stories'
        ordering = ['-created_at']


class StoryView(CreateUpdateBaseModel):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='story_view')
    profile_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                             related_name='viewed_stories')
    profile_obj_id = models.PositiveIntegerField()
    profile = GenericForeignKey('profile_content_type', 'profile_obj_id')
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"""{self.profile or self.profile.user.full_name} kordi
                {self.story.profile} ni storysini"""

    class Meta:
        unique_together = ('story', 'profile_content_type', 'profile_obj_id')
        ordering = ['-viewed_at']
        db_table = 'story_view'
        verbose_name = 'Story View'
        verbose_name_plural = 'Story Viewers'

