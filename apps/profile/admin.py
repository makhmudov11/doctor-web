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
# @admin.register(PatientProfile)
# class PatientProfileAdmin(admin.ModelAdmin):
#     list_display = [
#         'public_id',
#         'full_name',
#         'followers_count',
#         'following_count',
#         'posts_count',
#         'is_private',
#     ]
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
# @admin.register(DoctorProfile)
# class DoctorProfileAdmin(admin.ModelAdmin):
#     list_display = (
#         'public_id',
#         'full_name',
#         'specialization',
#         'experience_years',
#         'followers_count',
#         'is_private',
#     )
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
