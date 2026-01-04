from rest_framework.permissions import BasePermission

from apps.users.choices import CustomUserRoleChoices
from apps.utils.role_validate import RoleValidate


class VideoDestroyPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        profile = RoleValidate.get_profile_user(request)
        return bool(obj.profile == profile)


class DeleteVideoReactionPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        profile = RoleValidate.get_profile_user(request)
        return obj.profile == profile


class DeleteVideoReelsCommentPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        profile = RoleValidate.get_profile_user(request)
        return obj.profile == profile


class VideoReelsCommentReplyCreatePermission(BasePermission):
    def has_permission(self, request, view):
        return (
                request.user.is_authenticated and
                request.user.active_role == RoleValidate.get_token_active_role(request)
                and request.user.active_role in dict(CustomUserRoleChoices.choices)
        )

class UserAllVideoReelsPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        profile = RoleValidate.get_profile_user(request)
        return obj.profile == profile