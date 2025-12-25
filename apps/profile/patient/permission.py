from rest_framework.permissions import BasePermission

from apps.users.choices import CustomUserRoleChoices


class PatientPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and
                    request.user.active_role == CustomUserRoleChoices.BEMOR)

    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj.user)


