from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from apps.profile.serializers.profiles import GET_ROLE_SERIALIZER
from apps.utils.CustomValidationError import CustomValidationError
from apps.utils.role_validate import RoleValidate
from apps.video.choices import ReactionChoices
from apps.video.models import VideoReels, VideoReelsComment
from django.utils.translation import gettext_lazy as _

class VideoReelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoReels
        fields = '__all__'

class VideoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoReels
        fields = ['content', 'description', 'thumbnail']
        extra_kwargs = {
            "content" : {"required" : True},
            "description" : {"required" : True},
            "thumbnail" : {"required" : False},
        }

class VideoReactionSerializer(serializers.Serializer):
    reaction = serializers.ChoiceField(choices=ReactionChoices.choices)


class VideoCommentCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=2000, required=True)

    def validate(self, attrs):
        title = attrs.get('title', None)
        if title is None:
            raise CustomValidationError(
                detail=_("Comment kelishi shart")
            )
        return attrs


class VideoCommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    profile = serializers.SerializerMethodField()

    class Meta:
        model = VideoReelsComment
        fields = [
            'id',
            'title',
            'profile',
            'created_at',
            'replies'
        ]

    def get_replies(self, obj):
        qs = obj.replies.filter(is_active=True)
        return VideoCommentSerializer(qs, many=True).data

    def get_profile(self, obj):
        profile = RoleValidate.get_profile_user(self.context['request'])
        serializer = GET_ROLE_SERIALIZER.get(profile.user.active_role)
        return serializer(profile,
                          context={"request": self.context['request']}).data

class VideoCommentReplySerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, required=True)

    def create(self, validated_data):
        parent = self.context.get('parent')
        profile = self.context.get('profile')

        return VideoReelsComment.objects.create(
            parent=parent,
            content=parent.content,
            profile_obj_id=profile.id,
            profile_content_type=ContentType.objects.get_for_model(profile),
            **validated_data
        )


class VideoReelsCommentNestedSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = VideoReelsComment
        fields = ['id', 'title', 'parent', 'profile', 'created_at', 'replies']

    def get_profile(self, obj):
        profile = obj.profile
        serializer_class = GET_ROLE_SERIALIZER.get(profile.user.active_role)
        return {"profile" : profile.user.full_name}

    def get_replies(self, obj):
        queryset = obj.replies.filter(is_active=True).order_by('created_at')
        serializer = VideoReelsCommentNestedSerializer(
            queryset, many=True, context=self.context
        )
        return serializer.data

class CommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoReelsComment
        fields = ['content', 'parent', 'title', 'is_active', 'likes_count', 'dislikes_count']


class CommentSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = VideoReelsComment
        fields = ['id', 'profile', 'content', 'parent', 'title', 'is_active',
                  'likes_count', 'dislikes_count']



    def get_profile(self, obj):
        profile = RoleValidate.get_profile_user(self.context['request'])
        serializer = GET_ROLE_SERIALIZER.get(profile.user.active_role)
        return serializer(profile,
                          context={"request": self.context['request']}).data


class CommentReactionSerializer(serializers.Serializer):
    reaction = serializers.ChoiceField(choices=ReactionChoices.choices)

class VideoAllListSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = VideoReels
        fields = [
            'id', 'created_at', 'updated_at', 'deleted_at',
            'content', 'content_type', 'description', 'thumbnail',
            'duration', 'views_count', 'likes_count', 'dislikes_count',
            'comments_count', 'share_count', 'status',
            'profile'
        ]

    def get_profile(self, obj):
        request = self.context.get('request')
        profile = obj.profile  # GenericForeignKey orqali profile

        if not profile:
            return None
        serializer_class = GET_ROLE_SERIALIZER.get(profile.user.active_role)
        if not serializer_class:
            return None

        return serializer_class(profile, context={'request': request}).data
