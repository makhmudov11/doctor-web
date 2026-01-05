from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from apps.utils.CustomValidationError import CustomValidationError
from apps.utils.base_models import CreateUpdateBaseModel
from apps.video.choices import VideoReelsTypeChoices, ReactionChoices
from django.utils.translation import gettext_lazy as _

class VideoReels(CreateUpdateBaseModel):
    profile_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                             related_name='video_reels', verbose_name=_('Content egasi'))
    profile_obj_id = models.PositiveIntegerField()
    profile = GenericForeignKey('profile_content_type', 'profile_obj_id')
    content = models.FileField(upload_to='video_reels/', verbose_name=_('content manzili'))
    content_type = models.CharField(choices=VideoReelsTypeChoices.choices,
                                    default=VideoReelsTypeChoices.REELS, db_index=True,
                                    verbose_name=_('Content turi'))
    description = models.TextField(null=True, verbose_name=_('content haqida malumot'), db_index=True)
    thumbnail = models.ImageField(null=True, verbose_name=_('content oblojkasi'), upload_to='video_reels/thumbnail/')
    duration = models.PositiveIntegerField(default=0, verbose_name=_('content davomiyligi'))
    views_count = models.PositiveIntegerField(default=0, verbose_name=_('korishlar soni'))
    likes_count = models.PositiveIntegerField(default=0, verbose_name=_('likelar soni'))
    dislikes_count = models.PositiveIntegerField(default=0, verbose_name=_('dislikelar soni'))
    comments_count = models.PositiveIntegerField(default=0, verbose_name=_('jami izohlar soni'))
    share_count = models.PositiveIntegerField(default=0)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = _('video_reels')
        verbose_name = _("Video / Reel")
        verbose_name_plural = _("Video / Reels")
        ordering = ["-created_at"]

    def clean(self):
        if self.content_type == VideoReelsTypeChoices.REELS and self.duration > 60:
            raise CustomValidationError(
                detail="Reels turi uchun video davomiyligi 1 minutdan oshmasligi kerak."
            )

    def __str__(self):
        return self.description or self.pk


class VideoReelsView(CreateUpdateBaseModel):
    profile_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                             related_name='profile_video_reels')
    profile_obj_id = models.PositiveIntegerField()
    profile = GenericForeignKey('profile_content_type', 'profile_obj_id')
    content = models.ForeignKey(VideoReels, models.CASCADE, related_name='view_content')
    viewed_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = _('video_reels_view')
        verbose_name = _("Video / Reel/ View")
        verbose_name_plural = _("Video / Reels/ View")
        ordering = ["-created_at"]
        unique_together = ('profile_content_type', 'profile_obj_id', 'content')

    def __str__(self):
        return (f"{self.profile.user.fullname or self.pk} ko'rdi"
                f" {self.content.profile.full_name or self.content.pk}")


class VideoReaction(CreateUpdateBaseModel):
    profile_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                             related_name='profile_like_dislike')
    profile_obj_id = models.PositiveIntegerField()
    profile = GenericForeignKey('profile_content_type', 'profile_obj_id')
    content = models.ForeignKey(VideoReels, on_delete=models.CASCADE,
                                related_name='content_like_dislike', db_index=True)
    reaction = models.CharField(choices=ReactionChoices.choices, default=ReactionChoices.LIKE)

    class Meta:
        db_table = _('video_reaction')
        verbose_name = _("Video Reaction")
        verbose_name_plural = _("Video Reaction")
        ordering = ["-created_at"]
        unique_together = ('profile_content_type', 'profile_obj_id', 'content')

    def __str__(self):
        return f"{self.content.pk} --> {self.reaction}"


class VideoReelsComment(CreateUpdateBaseModel):
    content = models.ForeignKey(VideoReels, on_delete=models.CASCADE,
                                related_name='video_reels_comments', db_index=True)
    profile_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                             related_name='profile_comment')
    profile_obj_id = models.PositiveIntegerField()
    profile = GenericForeignKey('profile_content_type', 'profile_obj_id')
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="replies", null=True, blank=True, db_index=True
    )
    title = models.TextField()
    is_active = models.BooleanField(default=True)
    likes_count = models.PositiveIntegerField(default=0)
    dislikes_count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = _('comment')
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ["-created_at"]

    def __str__(self):
        return (f"{self.content.pk} contentga "
                f"{self.profile.user.full_name or ''} {self.title} izoh qoldirdi")


class CommentReaction(CreateUpdateBaseModel):
    comment = models.ForeignKey(VideoReelsComment, on_delete=models.CASCADE,
                                related_name='comment_reaction')
    profile_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                             related_name='profile_comment_reaction')
    profile_obj_id = models.PositiveIntegerField()
    profile = GenericForeignKey('profile_content_type', 'profile_obj_id')
    reaction = models.CharField(choices=ReactionChoices.choices, default=ReactionChoices.LIKE)

    class Meta:
        db_table = _('comment_reaction')
        verbose_name = _("Comment Reaction")
        verbose_name_plural = _("Comment Reactions")
        ordering = ["-created_at"]
        unique_together = ('profile_content_type', 'profile_obj_id', 'comment')

    def __str__(self):
        return f"{self.comment.pk} --> {self.reaction}"