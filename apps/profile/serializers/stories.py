from rest_framework import serializers

from apps.profile.models import Story, StoryView
from apps.profile.serializers.profiles import GET_ROLE_SERIALIZER
from apps.utils.CustomValidationError import CustomValidationError
from apps.utils.role_validate import RoleValidate


class UserStoryCreateSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Story
        fields = ['id', 'profile', 'content', 'content_type', 'view_count', 'expires_at', 'status',
                  'created_at', 'updated_at', 'deleted_at']
        extra_kwargs = {
            'profile': {'read_only': True},
            'content_type': {'read_only': True},
            'view_count': {'read_only': True},
            'expires_at': {'read_only': True},
            'status': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'deleted_at': {'read_only': True},
        }

    def get_profile(self, obj):
        role = RoleValidate.get_role(request=self.context['request'])
        serializer = GET_ROLE_SERIALIZER.get(role)
        return serializer(instance=RoleValidate.get_profile_user(self.context['request']),
                          context={"request" : self.context['request']}).data
    def validate(self, attrs):
        content = attrs.get('content')

        if not content:
            raise CustomValidationError(detail="Rasm yoki video fayl jo‘natilishi kerak")

        content_type = Story.media_type(content)

        if content_type is None:
            raise CustomValidationError(detail="Faqat rasm yoki video yuklash mumkin.")

        attrs['content_type'] = content_type
        return attrs


class UserStoryElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ['id', 'content', 'content_type', 'view_count', 'expires_at', 'created_at', 'updated_at', 'deleted_at']


class UserActiveStorySerializer(serializers.Serializer):
    profile = serializers.SerializerMethodField(read_only=True)
    stories = UserStoryElementSerializer(many=True, read_only=True)

    class Meta:
        model = Story
        fields = ['profile', 'stories']

    def get_profile(self, obj):
        role = RoleValidate.get_role(self.context['request'])
        serializer = GET_ROLE_SERIALIZER.get(role)
        return serializer(obj['profile'], context=self.context).data


class UserStoryListSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Story
        fields = ['id', 'profile', 'content', 'content_type', 'view_count',
                  'expires_at', 'status', 'created_at']

    def get_profile(self, obj):
        profile = obj.profile
        serializer = GET_ROLE_SERIALIZER.get(profile.user.active_role, None)
        if serializer is None:
            raise CustomValidationError(
                detail="Role aniqlanmadi"
            )
        return serializer(obj, context={"request" : self.context['request']}).data


class StoryViewSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = StoryView
        fields = ['profile', 'viewed_at']

    def get_profile(self, obj):
        profile = obj.profile
        serializer = GET_ROLE_SERIALIZER.get(profile.user.active_role, None)
        if serializer is None:
            raise CustomValidationError(
                detail="Role aniqlanmadi"
            )
        return serializer(obj, context={"request": self.context['request']}).data
