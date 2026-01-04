from rest_framework import serializers

from apps.profile.models import DoctorProfile

class AdminDoctorProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = '__all__'


class AdminDoctorProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = '__all__'


class AdminDoctorProfileRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = '__all__'



class AdminPatientProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = '__all__'


class AdminPatientProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = '__all__'


class AdminPatientProfileRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = '__all__'