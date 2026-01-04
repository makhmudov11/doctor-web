from django.contrib import admin

from apps.video.models import VideoReels, VideoReaction, VideoReelsComment


# Register your models here.

@admin.register(VideoReels)
class VideoReelsAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'content_type', 'duration', 'profile', 'status',
                    'description', 'thumbnail', 'views_count', 'likes_count', 'dislikes_count', 'comments_count']


@admin.register(VideoReaction)
class VideoReactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'reaction', 'content', 'profile']

@admin.register(VideoReelsComment)
class VideoReelsCommentAdmin(admin.ModelAdmin):
    list_display = ['id','content', 'profile', 'parent', 'title', 'is_active', 'likes_count', 'dislikes_count']