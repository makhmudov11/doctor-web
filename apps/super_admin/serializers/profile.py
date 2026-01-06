from rest_framework import serializers

from apps.profile.models import DoctorProfile, PatientProfile
from apps.users.serializers.user_detail import UserListSerializer


class AdminDoctorProfileListSerializer(serializers.ModelSerializer):

    user = UserListSerializer(read_only=True)

    class Meta:
        model = DoctorProfile
        fields = [
            "public_id", "user", "username", "specialization",
            "experience_years", "following_count", "followers_count",
            "posts_count", "created_at", "updated_at", "deleted_at", ]



class AdminPatientProfileListSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)

    class Meta:
        model = PatientProfile
        fields = ['public_id', 'user', 'following_count', 'slug', 'status']