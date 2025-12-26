from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.profile.choices import FollowChoices
from apps.profile.follow.models import Follow
from apps.profile.patient.models import PatientProfile


@receiver(post_save, sender=Follow)
def update_follow_count(sender, instance, created, **kwargs):
    if created:
        #following
        content_type = ContentType.objects.get_for_model(instance.profile)
        instance.profile.following_count = Follow.objects.filter(
            profile_content_type=content_type,
            profile_obj_id=instance.profile.id,
            status=FollowChoices.FOLLOW
        ).count()
        instance.profile.save(update_fields=['following_count'])

        #followers
        instance.following.followers_count = Follow.objects.filter(
            following=instance.following,
            status=FollowChoices.FOLLOW
        ).count()
        instance.following.save(update_fields=['followers_count'])


from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Follow, PatientProfile


@receiver(pre_save, sender=Follow)
def update_follow_count(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Follow.objects.get(pk=instance.pk)

        if old_instance.status == FollowChoices.FOLLOW and instance.status == FollowChoices.UNFOLLOW:
            try:
                instance.following.followers_count -= 1
                instance.profile.following_count -= 1
                instance.profile.save(update_fields=['following_count'])
                instance.following.save(update_fields=['followers_count'])
            except PatientProfile.DoesNotExist:
                pass
        elif old_instance.status == FollowChoices.UNFOLLOW and instance.status == FollowChoices.FOLLOW:
            try:
                instance.following.followers_count += 1
                instance.profile.following_count += 1
                instance.profile.save(update_fields=['following_count'])
                instance.following.save(update_fields=['followers_count'])
            except PatientProfile.DoesNotExist:
                pass