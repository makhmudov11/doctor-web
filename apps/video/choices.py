from django.db import models


class VideoReelsTypeChoices(models.TextChoices):
    REELS = 'reels', 'Reels'
    VIDEO = 'video', 'Video'


class ReactionChoices(models.TextChoices):
    LIKE = 'like', 'Like'
    DISLIKE = 'dislike', 'DisLike'