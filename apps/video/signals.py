import tempfile

from django.db import transaction
from django.db.models import F, Count
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from moviepy import VideoFileClip

from apps.utils.CustomValidationError import CustomValidationError
from apps.video.choices import ReactionChoices
from apps.video.models import VideoReels, VideoReaction, VideoReelsComment, CommentReaction, VideoReelsView


@receiver(pre_save, sender=VideoReels)
def set_duration(sender, instance, **kwargs):
    if instance.content and not instance.duration:
        instance.content.seek(0)

        # Windows-friendly tempfile
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp:
            for chunk in instance.content.chunks():
                temp.write(chunk)
            temp.flush()

            # VideoFileClip bilan duration olish
            clip = VideoFileClip(temp.name)
            try:
                instance.duration = int(clip.duration) + 1
            finally:
                clip.close()  # video + audio readerlar ham yopiladi

            if instance.duration > 60:
                raise CustomValidationError(
                    detail="Reels davomiyligi 60 sekunddan katta bo'lishi mumkin enas"
                )


def recalc_video_reactions(video):
    counts = dict(VideoReaction.objects.filter(content=video).values_list('reaction').annotate(c=Count('id')))
    VideoReels.objects.filter(id=video.id).update(likes_count=counts.get(ReactionChoices.LIKE, 0),
                                                  dislikes_count=counts.get(ReactionChoices.DISLIKE, 0))


@receiver(post_save, sender=VideoReaction)
def update_video_reaction_count(sender, instance, **kwargs):
    transaction.on_commit(lambda: recalc_video_reactions(instance.content))


@receiver(post_delete, sender=VideoReaction)
def delete_reaction_video(sender, instance, **kwargs):
    transaction.on_commit(lambda: recalc_video_reactions(instance.content))


@receiver(post_save, sender=VideoReelsComment)
def update_video_comments_count(sender, instance, created, **kwargs):
    video = instance.content
    comments_count = VideoReelsComment.objects.filter(
        content=video,
        is_active=True
    ).count()
    video.comments_count = comments_count
    video.save(update_fields=['comments_count'])

@receiver([post_save, post_delete], sender=CommentReaction)
def recalc_comment_reactions(sender, instance, **kwargs):
    comment = instance.comment

    counts = dict(
        CommentReaction.objects
        .filter(comment=comment)
        .values_list('reaction')
        .annotate(c=Count('id'))
    )

    comment.likes_count = counts.get(ReactionChoices.LIKE, 0)
    comment.dislikes_count = counts.get(ReactionChoices.DISLIKE, 0)

    comment.save(update_fields=['likes_count', 'dislikes_count'])

@receiver(post_save, sender=VideoReelsView)
def recalc_video_views(sender, instance, **kwargs):
    video = instance.content
    video.views_count = video.view_content.count()
    video.save(update_fields=['views_count'])