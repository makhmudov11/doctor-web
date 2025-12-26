from rest_framework import serializers

from apps.profile.doctor.serializers import DoctorProfileSerializer
from apps.profile.follow.models import Follow
from apps.profile.patient.models import PatientProfile
from apps.users.serializers.user_detail import UserListSerializer
from apps.utils.CustomValidationError import CustomValidationError

class PatientProfileSerializer(serializers.ModelSerializer):
    user = UserListSerializer()

    class Meta:
        model = PatientProfile
        fields = ['id', 'public_id', 'following_count', 'user']









class PatientFollowUserSerializer(serializers.Serializer):
    profile = PatientProfileSerializer(read_only=True)
    follows = DoctorProfileSerializer(source='following', read_only=True)

    class Meta:
        model = Follow
        fields = ['profile', 'follows']


    def validate(self, attrs):
        profile_public_id = self.context.get('profile_public_id')
        if profile_public_id is None:
            raise CustomValidationError(
                detail='Profile public id kelishi shart'
            )
        if isinstance(profile_public_id, int):
            return CustomValidationError(detail="Public id integer bo'lishi kerak")
        return attrs



class PatientUnFollowUserSerializer(serializers.Serializer):

    def validate(self, attrs):
        profile_public_id = self.context.get('profile_public_id')
        if not profile_public_id:
            raise CustomValidationError(
                detail='Profile public id kelishi shart'
            )
        return attrs



