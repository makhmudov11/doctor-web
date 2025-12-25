from rest_framework import serializers

from apps.profile.doctor.serializers import DoctorProfileSerializer
from apps.profile.follow.models import Follow
from apps.profile.patient.models import PatientProfile
from apps.users.serializers.user_detail import UserListSerializer
from apps.utils.CustomValidationError import CustomValidationError


class PatientFollowListSerializer(serializers.ModelSerializer):
    user = UserListSerializer(source='profile.user')
    follows = DoctorProfileSerializer(source='following', many=True)

    class Meta:
        model = Follow
        fields = ['user', 'follows']



class PatientFollowUserSerializer(serializers.Serializer):
    profile_public_id = serializers.CharField(max_length=50)

    def validate(self, attrs):
        profile_public_id = attrs.get('profile_public_id')
        if not profile_public_id:
            raise CustomValidationError(
                detail='Profile public id kelishi shart'
            )
        return attrs

    def save(self, **kwargs):
        patient_profile = self.context['request'].user.patient_profile
        if not isinstance(patient_profile, PatientProfile):
            raise CustomValidationError(
                detail='Userga tegishli profile mavjud emas'
            )
        self.following_count = Follow.get_follow_count(profile=patient_profile) + 1
        super().save(**kwargs)
