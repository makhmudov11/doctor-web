from rest_framework import serializers

from apps.profile.models import DoctorProfile


class AdminDoctorProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = '__all__'


class AdminPatientProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = '__all__'
