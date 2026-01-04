from rest_framework.permissions import BasePermission

from apps.users.choices import CustomUserRoleChoices
from apps.utils.role_validate import RoleValidate


class IsDoctor(BasePermission):
    def has_permission(self, request, view):

        return (request.user.is_authenticated and
                request.user.active_role == RoleValidate.get_token_active_role(request)
                and request.user.active_role == CustomUserRoleChoices.SHIFOKOR
                )


class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and
                request.user.active_role == RoleValidate.get_token_active_role(request)
                and request.user.active_role == CustomUserRoleChoices.BEMOR
                )


class DoctorStoryPermission(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and
                 request.user.active_role == RoleValidate.get_token_active_role(request)
                and request.user.active_role == CustomUserRoleChoices.SHIFOKOR

                )

    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj.profile.user)


class PatientProfilePermission(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and
                request.user.active_role == RoleValidate.get_token_active_role(request)
                and request.user.active_role == CustomUserRoleChoices.BEMOR
                )

    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj.user)


class DoctorProfilePermission(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and
                request.user.active_role == RoleValidate.get_token_active_role(request)
                and request.user.active_role == CustomUserRoleChoices.SHIFOKOR
                )

    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj.user)


class UserFollowListPermission(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and
                request.user.active_role == RoleValidate.get_token_active_role(request)
                and request.user.active_role in dict(CustomUserRoleChoices.choices)
                )


class UserProfilePermission(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and
                request.user.active_role == RoleValidate.get_token_active_role(request)
                and request.user.active_role in dict(CustomUserRoleChoices.choices)
                )

    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj.user)
