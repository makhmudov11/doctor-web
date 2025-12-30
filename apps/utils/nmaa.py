from apps.profile.serializers.profiles import PatientProfileSerializer, DoctorProfileSerializer
from apps.users.choices import CustomUserRoleChoices



GET_ROLE_SERIALIZER = {
    CustomUserRoleChoices.BEMOR : PatientProfileSerializer,
    CustomUserRoleChoices.SHIFOKOR : DoctorProfileSerializer
}