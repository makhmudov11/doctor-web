from rest_framework import serializers

from apps.profile.models import Follow
from apps.profile.serializers.profiles import GET_ROLE_SERIALIZER, DoctorProfileSerializer, PatientProfileSerializer
from apps.users.choices import CustomUserRoleChoices
from apps.utils.CustomValidationError import CustomValidationError
from apps.utils.role_validate import RoleValidate


class UserFollowCreateSerializer(serializers.Serializer):
    profile = serializers.SerializerMethodField(read_only=True)
    follows = DoctorProfileSerializer(source='following', read_only=True)

    class Meta:
        model = Follow
        fields = ['profile', 'follows']

    def get_profile(self, obj):
        role = RoleValidate.get_role(self.context['request'])
        serializer = GET_ROLE_SERIALIZER.get(role)
        return serializer(instance=obj.profile, context={"request": self.context['request']}).data


    def validate(self, attrs):
        profile_public_id = self.context.get('profile_public_id')
        if profile_public_id is None:
            raise CustomValidationError(
                detail='Profile public id kelishi shart'
            )
        try:
            self.context['profile_public_id'] = int(profile_public_id)
        except ValueError:
            raise CustomValidationError(detail="Public id integer bo'lishi kerak")
        return attrs

class UserUnFollowUserSerializer(serializers.Serializer):

    def validate(self, attrs):
        profile_public_id = self.context.get('profile_public_id')
        if not profile_public_id:
            raise CustomValidationError(
                detail='Profile public id kelishi shart'
            )
        return attrs


class UserFollowersListSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField(read_only=True, source='profile')

    class Meta:
        model = Follow
        fields = ['followers']

    def get_followers(self, obj):
        if obj.user.active_role == CustomUserRoleChoices.SHIFOKOR:
            print()
            return DoctorProfileSerializer(obj).data
        elif obj.user.active_role == CustomUserRoleChoices.BEMOR:
            return PatientProfileSerializer(obj).data
        else:
            raise CustomValidationError(
                detail="User ro'li aniqlanmadi"
            )




# class PatientFollowUserSerializer(serializers.Serializer):
#     profile = PatientProfileSerializer(read_only=True)
#     follows = DoctorProfileSerializer(source='following', read_only=True)
#
#     class Meta:
#         model = Follow
#         fields = ['profile', 'follows']
#
#     def validate(self, attrs):
#         profile_public_id = self.context.get('profile_public_id')
#         if profile_public_id is None:
#             raise CustomValidationError(
#                 detail='Profile public id kelishi shart'
#             )
#         if not isinstance(profile_public_id, int):
#             return CustomValidationError(detail="Public id integer bo'lishi kerak")
#         return attrs
#
#
# class PatientUnFollowUserSerializer(serializers.Serializer):
#
#     def validate(self, attrs):
#         profile_public_id = self.context.get('profile_public_id')
#         if not profile_public_id:
#             raise CustomValidationError(
#                 detail='Profile public id kelishi shart'
#             )
#         return attrs
