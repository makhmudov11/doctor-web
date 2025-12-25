from django.db import models


class ProfilePrivateChoices(models.TextChoices):
    PENDING = 'pending', 'Pending'
    APPROVED = 'approved', 'Approved'
    REJECTED = 'rejected', 'Rejected'


class StoryChoices(models.TextChoices):
    IMAGE = 'image', 'Image'
    VIDEO = 'video', 'Video'


class PubChoices(models.TextChoices):
    IMAGE = 'reels', 'Reels'
    VIDEO = 'video', 'Video'


class FollowChoices(models.TextChoices):
    FOLLOW = 'follow', 'Follow'
    UNFOLLOW = 'unfollow', 'Unfollow'
    BLOCK = 'blocked', 'Blocked'