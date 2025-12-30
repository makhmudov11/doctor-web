from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken

from apps.profile.models import DoctorProfile, PatientProfile
from apps.users.choices import CustomUserRoleChoices
from apps.utils.CustomValidationError import CustomValidationError


class RoleValidate:

    @classmethod
    def get_token_active_role(cls, request):
        token = request.headers.get('Authorization')
        if not token:
            raise AuthenticationFailed('Token not found')
        try:
            token = token.split(' ')[1]
            access_token = AccessToken(token)
            return access_token['active_role']
        except Exception as e:
            raise AuthenticationFailed(f'Invalid token: {str(e)}')

    @classmethod
    def get_profile_user(cls, request):
        role = cls.get_role(request)
        try:
            if role == CustomUserRoleChoices.BEMOR:
                return request.user.patient_profile
            elif role == CustomUserRoleChoices.SHIFOKOR:
                return request.user.doctor_profile
            else:
                raise CustomValidationError(detail="User roli aniqlanmadi")
        except ObjectDoesNotExist:
            raise CustomValidationError(detail="Userga tegishli profile topilmadi")

    @classmethod
    def get_role_model(cls, request):
        role = request.user.active_role
        if role == CustomUserRoleChoices.BEMOR:
            return PatientProfile
        elif role == CustomUserRoleChoices.SHIFOKOR:
            return DoctorProfile
        else:
            raise CustomValidationError(detail='Role aniqlanmadi')

    @classmethod
    def get_role(cls, request):
        token_role = cls.get_token_active_role(request)
        user_role = request.user.active_role
        if token_role != user_role:
            raise CustomValidationError(detail='Token bu role uchun emas')
        return user_role
