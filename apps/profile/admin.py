# from django.contrib import admin
# from apps.profile.models import  BaseProfile, PatientProfile, DoctorProfile
#
#
# @admin.register(BaseProfile)
# class BaseProfileAdmin(admin.ModelAdmin):
#     list_display = (
#         'public_id',
#         'full_name',
#         'user',
#         'followers_count',
#         'following_count',
#         'posts_count',
#         'is_private',
#     )
#
#     search_fields = ('user__username', 'full_name', 'user__contact')
#     list_filter = ('is_private', 'role')
#     ordering = ('-created_at',)
#
#
from django.contrib import admin

from apps.profile.doctor.models import DoctorProfile
from apps.profile.follow.models import Follow
from apps.profile.patient.models import PatientProfile


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = [
        'public_id',
        'user_full_name', #method
        'following_count',
     ]

    def user_full_name(self, obj):
        return obj.user.full_name
#
#     search_fields = (
#         'profile__full_name',
#         'profile__user__contact',
#     )
#
#     list_filter = ('profile__is_private',)
#     ordering = ('-created_at',)
#
#     def public_id(self, obj):
#         return obj.profile.public_id
#
#     def full_name(self, obj):
#         return obj.profile.full_name
#
#     def followers_count(self, obj):
#         return obj.profile.followers_count
#
#     def following_count(self, obj):
#         return obj.profile.following_count
#
#     def posts_count(self, obj):
#         return obj.profile.posts_count
#
#     def is_private(self, obj):
#         return obj.profile.is_private
#
#
@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = (
        'public_id',
        'user_full_name', #method
        'specialization',
        'experience_years',
        'followers_count',
        'is_private',
    )

    def user_full_name(self, obj):
        return obj.user.full_name



@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['profile', 'following', 'status', 'created_at']

    def show_profile(self, obj):
        if obj.profile:
            return obj.profile.user.full_name
        return obj.id


    def show_following(self, obj):
        if obj.following:
            return obj.following.user.full_name
        return obj.id


#
#     search_fields = (
#         'profile__full_name',
#         'profile__user__contact',
#     )
#
#     list_filter = ('profile__is_private',)
#     ordering = ('-created_at',)
#
#     def public_id(self, obj):
#         return obj.profile.public_id
#
#     def full_name(self, obj):
#         return obj.profile.full_name
#
#     def followers_count(self, obj):
#         return obj.profile.followers_count
#
#     def is_private(self, obj):
#         return obj.profile.is_private
#
#
# # @admin.register(Story)
# # class StoryAdmin(admin.ModelAdmin):
# #     list_display = ['id', 'public_id', 'profile', 'content_type', 'view_count', 'expires_at', 'is_expired_display']
# #     search_fields = ['profile__username', 'profile__full_name']
# #     list_filter = ['content_type']
# #     list_per_page = 20
# #     ordering = ['-created_at']
# #     readonly_fields = ['view_count']
# #
# #     def is_expired_display(self, obj):
# #         return obj.is_expired()
# #
# #     is_expired_display.boolean = True
# #     is_expired_display.short_description = 'EXPIRED'
# #
# #
# # @admin.register(StoryView)
# # class StoryViewAdmin(admin.ModelAdmin):
# #     list_display = ('story', 'view_profile', 'viewed_at')
# #     search_fields = ('story__profile__username', 'view_profile__username')
# #     list_filter = ('story__content_type', 'viewed_at')
# #     list_per_page = 20
# #     ordering = ('-viewed_at',)
