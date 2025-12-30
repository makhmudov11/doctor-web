from django.contrib import admin

from apps.profile.models import PatientProfile, DoctorProfile, Follow, Story, StoryView
from apps.utils.role_validate import RoleValidate


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = [
        'public_id',
        'user_full_name',  # method
        'following_count',
    ]

    def user_full_name(self, obj):
        return obj.user.full_name


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = (
        'public_id',
        'user_full_name',  # method
        'specialization',
        'experience_years',
        'following_count',
        'followers_count',
        'is_private',
    )

    def user_full_name(self, obj):
        return obj.user.full_name


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['show_profile','get_profile_type', 'following', 'get_follow_user_type', 'status', 'created_at']

    def show_profile(self, obj):
        if obj.profile:
            return obj.profile.public_id
        return obj.id
    show_profile.short_description = 'Profile Public ID'

    def get_profile_type(self, obj):
        if obj.profile:
            return obj.profile.__class__.__name__
        return None
    get_profile_type.short_description = 'Profile Type'

    def get_follow_user_type(self, obj):
        if obj.following:
            return obj.following.__class__.__name__
        return None

    get_profile_type.short_description = 'Following Profile Type'



    def show_following(self, obj):
        if obj.following:
            return obj.following.user.full_name
        return obj.id


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_profile_id', 'content_type', 'view_count', 'expires_at', 'is_expired_display']
    search_fields = ['profile', 'profile']
    list_filter = ['content_type']
    list_per_page = 20
    ordering = ['-created_at']
    readonly_fields = ['view_count']

    def is_expired_display(self, obj):
        return obj.is_expired()

    def get_profile_id(self, obj):
        return obj.profile.public_id if obj.profile else None

    get_profile_id.short_description = 'Profile ID'

    is_expired_display.boolean = True
    is_expired_display.short_description = 'EXPIRED'


@admin.register(StoryView)
class StoryViewAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_story', 'profile', 'viewed_at')
    list_filter = ('viewed_at', 'story')
    search_fields = ('profile_obj_id',)
    readonly_fields = ('viewed_at',)

    def get_story(self, obj):
        return obj.story.id

    get_story.short_description = 'Story ID'