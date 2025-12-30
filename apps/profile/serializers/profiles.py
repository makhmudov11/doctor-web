from rest_framework import serializers

from apps.profile.models import PatientProfile, DoctorProfile
from apps.users.choices import CustomUserRoleChoices
from apps.users.serializers.user_detail import UserListSerializer


class PatientProfileSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)

    class Meta:
        model = PatientProfile
        fields = ['public_id', 'user', 'following_count', 'slug', 'status']


class DoctorProfileSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)

    class Meta:
        model = DoctorProfile
        fields = [
            "public_id", "user", "username", "specialization",
            "experience_years", "following_count", "followers_count",
            "posts_count", "created_at", "updated_at", "deleted_at", ]


GET_ROLE_SERIALIZER = {
    CustomUserRoleChoices.BEMOR : PatientProfileSerializer,
    CustomUserRoleChoices.SHIFOKOR : DoctorProfileSerializer
}