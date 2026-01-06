from rest_framework import serializers

from apps.history.models import Address
from apps.history.serializers.address import AddressFullDataSerializer
from apps.profile.models import DoctorProfile, PatientProfile
from apps.users.serializers.user_detail import UserListSerializer, UserFullDataSerializer


class AdminDoctorProfileListSerializer(serializers.ModelSerializer):

    user = UserListSerializer(read_only=True)

    class Meta:
        model = DoctorProfile
        fields = [
            "public_id", "user", "username", "specialization",
            "experience_years", "following_count", "followers_count",
            "posts_count", "created_at", "updated_at", "deleted_at", ]



class AdminPatientProfileListSerializer(serializers.ModelSerializer):
    user = UserFullDataSerializer(read_only=True)
    addresses = serializers.SerializerMethodField()

    class Meta:
        model = PatientProfile
        fields = ['public_id', 'user', 'following_count', 'slug', 'status', 'created_at', 'updated_at', 'deleted_at',
                  'addresses']

    def get_addresses(self, obj):
        return AddressFullDataSerializer(obj.patient_address.all(), many=True).data