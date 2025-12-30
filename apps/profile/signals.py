from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from apps.profile.choices import FollowChoices
from apps.profile.models import Follow, PatientProfile, StoryView
from apps.utils.CustomResponse import CustomResponse


@receiver(post_save, sender=Follow)
def update_follow_count(sender, instance, created, **kwargs):
    if created:
        # following
        content_type = ContentType.objects.get_for_model(instance.profile)
        instance.profile.following_count = Follow.objects.filter(
            profile_content_type=content_type,
            profile_obj_id=instance.profile.id,
            status=FollowChoices.FOLLOW
        ).count()
        instance.profile.save(update_fields=['following_count'])

        # followers
        instance.following.followers_count = Follow.objects.filter(
            following=instance.following,
            status=FollowChoices.FOLLOW
        ).count()
        instance.following.save(update_fields=['followers_count'])


@receiver(pre_save, sender=Follow)
def update_unfollow_count(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Follow.objects.get(pk=instance.pk)
        except Follow.DoesNotExist:
            return CustomResponse.error_response(message='Obyekt topilmadi')
        if old_instance.status == FollowChoices.FOLLOW and instance.status == FollowChoices.UNFOLLOW:
            try:
                instance.following.followers_count -= 1
                instance.profile.following_count -= 1
                instance.profile.save(update_fields=['following_count'])
                instance.following.save(update_fields=['followers_count'])
            except PatientProfile.DoesNotExist:
                return CustomResponse.error_response(message='Bemor profili topilmadi')
        elif old_instance.status == FollowChoices.UNFOLLOW and instance.status == FollowChoices.FOLLOW:
            try:
                instance.following.followers_count += 1
                instance.profile.following_count += 1
                instance.profile.save(update_fields=['following_count'])
                instance.following.save(update_fields=['followers_count'])
            except PatientProfile.DoesNotExist:
                return CustomResponse.error_response(message='Bemor profili topilmadi')


@receiver(post_save, sender=StoryView)
def story_view_count(sender, instance, created, **kwargs):
    try:
        profile = instance.story.profile
    except Exception as e:
        return CustomResponse.error_response(message='Profile topilmadi')
    if created:
        view_count = StoryView.objects.filter(story=instance.story).count()
        instance.story.view_count = view_count
        instance.story.save(update_fields=['view_count'])
