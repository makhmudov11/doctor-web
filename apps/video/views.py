from django.contrib.contenttypes.models import ContentType
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from django.utils.translation import gettext_lazy as _

from apps.profile.paginations import DoctorProfileListPagination
from apps.profile.permission import IsDoctor, UserProfilePermission
from apps.utils.CustomResponse import CustomResponse
from apps.utils.role_validate import RoleValidate
from apps.video.choices import VideoReelsTypeChoices, ReactionChoices
from apps.video.models import VideoReels, VideoReaction, VideoReelsComment, CommentReaction, VideoReelsView
from apps.video.permission import VideoDestroyPermission, \
    DeleteVideoReelsCommentPermission, VideoReelsCommentReplyCreatePermission, UserAllVideoReelsPermission
from apps.video.serializers import VideoReelsSerializer, VideoCreateSerializer, \
    VideoCommentCreateSerializer, VideoCommentReplySerializer, CommentSerializer, \
    VideoReelsCommentNestedSerializer, CommentReactionSerializer, VideoAllListSerializer


class VideoCreateAPIView(CreateAPIView):
    """
    Video post yaratish
    """
    queryset = VideoReels.objects.all()
    permission_classes = [IsDoctor]
    serializer_class = VideoCreateSerializer
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        video = self.perform_create(serializer)
        full_serializer = VideoReelsSerializer(video, context={'request': request})
        return CustomResponse.success_response(
            data=full_serializer.data,
            message="Video yaratildi"
        )

    def perform_create(self, serializer):
        profile = RoleValidate.get_profile_user(self.request)
        return serializer.save(content_type=VideoReelsTypeChoices.VIDEO,
                               profile_content_type=ContentType.objects.get_for_model(profile),
                               profile_obj_id=profile.id
                               )

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return self.serializer_class
        return VideoReelsSerializer


class VideoDestroyAPIView(DestroyAPIView):
    """
    Videoni o'chirish
    """
    permission_classes = [VideoDestroyPermission]

    def get_object(self):
        video_id = self.kwargs.get('video_id')
        return VideoReels.objects.filter(id=video_id, status=True).first()

    def destroy(self, request, *args, **kwargs):
        video_id = kwargs.get('video_id', None)
        if video_id is None:
            return CustomResponse.error_response(
                message=_("Video id kelishi shart")
            )
        video = self.get_object()
        if not video:
            return CustomResponse.error_response(
                message=_("Video topilmadi")
            )
        self.check_object_permissions(request, video)
        self.perform_destroy(video)
        return CustomResponse.success_response(
            message=_("Video muvaffaqiyatli ochirildi"),
            code=status.HTTP_204_NO_CONTENT
        )


class ReelsCreateAPIView(CreateAPIView):
    """
    Reels yaratish
    """
    queryset = VideoReels.objects.all()
    permission_classes = [IsDoctor]
    serializer_class = VideoCreateSerializer
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        video = self.perform_create(serializer)
        full_serializer = VideoReelsSerializer(video, context={'request': request})
        return CustomResponse.success_response(
            data=full_serializer.data,
            message="Reels yaratildi"
        )

    def perform_create(self, serializer):
        profile = RoleValidate.get_profile_user(self.request)
        return serializer.save(content_type=VideoReelsTypeChoices.VIDEO,
                               profile_content_type=ContentType.objects.get_for_model(profile),
                               profile_obj_id=profile.id
                               )

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return self.serializer_class
        return VideoReelsSerializer


class VideoReactionAPIView(APIView):
    permission_classes = [UserProfilePermission]

    def post(self, request, video_id):
        reaction_type = request.data.get('reaction', None)
        if reaction_type not in ReactionChoices.values:
            return CustomResponse.error_response(
                message=_("Reaksiya turi xato"),
                code=status.HTTP_400_BAD_REQUEST
            )

        video = VideoReels.objects.filter(id=video_id).first()
        if not video:
            return CustomResponse.error_response(
                message=_("Video topilmadi"),
                code=status.HTTP_404_NOT_FOUND
            )

        profile = RoleValidate.get_profile_user(request)
        ct = ContentType.objects.get_for_model(profile)

        obj = VideoReaction.objects.filter(
            profile_content_type=ct,
            profile_obj_id=profile.id,
            content=video
        ).first()

        if obj and obj.reaction == reaction_type:
            obj.delete()
            return CustomResponse.success_response(
                message=_("Reaksiya o‘chirildi"),
                data={"reaction": None}
            )

        if obj:
            obj.reaction = reaction_type
            obj.save(update_fields=['reaction'])
            return CustomResponse.success_response(
                message=_("Reaksiya yangilandi"),
                data={"reaction": reaction_type}
            )

        VideoReaction.objects.create(
            profile_content_type=ct,
            profile_obj_id=profile.id,
            content=video,
            reaction=reaction_type
        )
        return CustomResponse.success_response(
            message=_("Reaksiya qo‘shildi"),
            data={"reaction": reaction_type}
        )


class VideoCommentCreateAPIView(APIView):
    """
    Comment qoldirish
    """
    permission_classes = [UserProfilePermission]
    serializer_class = VideoCommentCreateSerializer

    def post(self, request, video_id):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not video_id:
            return CustomResponse.error_response(
                message=_("Video id kelishi shart"),
                code=status.HTTP_400_BAD_REQUEST
            )

        try:
            video = VideoReels.objects.filter(id=video_id).first()
        except VideoReels.DoesNotExist:
            return CustomResponse.error_response(message="Video topilmadi",
                                                 code=status.HTTP_404_NOT_FOUND)

        profile = RoleValidate.get_profile_user(request)

        commet_obj = VideoReelsComment.objects.create(
            content=video,
            profile_content_type=ContentType.objects.get_for_model(profile),
            profile_obj_id=profile.id,
            title=serializer.validated_data['title'],
        )

        return CustomResponse.success_response(
            message="Izoh qoldirildi",
            data=CommentSerializer(instance=commet_obj, context={"request": request}).data
        )


class VideoCommentListAPIView(APIView):
    serializer_class = CommentSerializer
    permission_classes = []

    def get(self, request, video_id):
        video = VideoReels.objects.filter(id=video_id).first()
        if not video:
            return CustomResponse.error_response(message=_("Video topilmadi"))

        comments = VideoReelsComment.objects.filter(
            content=video,
            parent__isnull=True,
            is_active=True
        )

        serializer = self.serializer_class(comments, many=True, context={"request": request})
        return CustomResponse.success_response(data=serializer.data)


class DeleteVideoReelsCommentDestroyAPIView(DestroyAPIView):
    permission_classes = [DeleteVideoReelsCommentPermission]

    def get_object(self):
        comment_id = self.kwargs.get('comment_id', None)
        profile = RoleValidate.get_profile_user(self.request)
        return VideoReelsComment.objects.filter(
            id=comment_id,
            profile_content_type=ContentType.objects.get_for_model(profile),
            profile_obj_id=profile.id,
            is_active=True
        ).first()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            return CustomResponse.error_response(
                message=_("Comment topilmadi")
            )
        self.perform_destroy(instance)
        return CustomResponse.success_response(code=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save(update_fields=['is_active'])


class VideoReelsCommentReplyAPIView(APIView):
    serializer_class = VideoCommentReplySerializer
    permission_classes = [VideoReelsCommentReplyCreatePermission]

    def post(self, request, comment_id):
        if not comment_id:
            return CustomResponse.error_response(
                message=_("Comment id kelishi shart"),
                code=status.HTTP_400_BAD_REQUEST
            )
        try:
            parent = VideoReelsComment.objects.get(
                id=comment_id,
                is_active=True
            )
        except VideoReelsComment.DoesNotExist:
            return CustomResponse.error_response("Parent comment topilmadi")

        profile = RoleValidate.get_profile_user(request)

        serializer = self.serializer_class(data=request.data,
                                           context={
                                               "profile": profile,
                                               "parent": parent,
                                               "comment_id": comment_id
                                           })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponse.success_response(
            message=_("Comment muvaffaqiyatli yaratildi"),
            data=serializer.data,
            code=status.HTTP_201_CREATED
        )


class VideoReelsCommentReplyListAPIView(ListAPIView):
    serializer_class = VideoReelsCommentNestedSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        comment_id = self.kwargs.get('comment_id', None)
        if comment_id is None:
            return CustomResponse.error_response(
                message=_("Comment id kelishi shart")
            )
        return VideoReelsComment.objects.filter(
            parent_id=comment_id,
            is_active=True
        ).order_by('created_at')


class CommentReactionAPIView(APIView):
    permission_classes = [UserProfilePermission]
    serializer_class = CommentReactionSerializer

    def post(self, request, comment_id):
        reaction = request.data.get('reaction')

        if reaction not in dict(ReactionChoices.choices):
            return CustomResponse.error_response("Reaction noto‘g‘ri")

        try:
            comment = VideoReelsComment.objects.get(
                id=comment_id,
                is_active=True
            )
        except VideoReelsComment.DoesNotExist:
            return CustomResponse.error_response(message=_("Comment topilmadi"))

        profile = RoleValidate.get_profile_user(request)
        ct = ContentType.objects.get_for_model(profile)

        obj = CommentReaction.objects.filter(
            comment=comment,
            profile_content_type=ct,
            profile_obj_id=profile.id
        ).first()

        if obj and obj.reaction == reaction:
            obj.delete()
            return CustomResponse.success_response(
                message="Reaction o‘chirildi",
                data={"reaction": None}
            )

        if obj:
            obj.reaction = reaction
            obj.save(update_fields=['reaction'])
            return CustomResponse.success_response(
                message="Reaction yangilandi",
                data={"reaction": reaction}
            )

        CommentReaction.objects.create(
            comment=comment,
            profile_content_type=ct,
            profile_obj_id=profile.id,
            reaction=reaction
        )

        return CustomResponse.success_response(
            message="Reaction qo‘shildi",
            data={"reaction": reaction},
            code=status.HTTP_201_CREATED
        )


class VideoAllListAPIView(ListAPIView):
    serializer_class = VideoAllListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return VideoReels.objects.filter(
            content_type=VideoReelsTypeChoices.VIDEO
        )

    pagination_class = DoctorProfileListPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['description', 'profile', 'content_type']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['id']


class UserVideoListAPIView(ListAPIView):
    serializer_class = VideoAllListSerializer
    permission_classes = [UserAllVideoReelsPermission]

    def get_queryset(self):
        profile = RoleValidate.get_profile_user(self.request)
        return VideoReels.objects.filter(
            profile_content_type=ContentType.objects.get_for_model(profile),
            profile_obj_id=profile.id,
            content_type=VideoReelsTypeChoices.VIDEO
        )


class ReelsAllListAPIView(ListAPIView):
    serializer_class = VideoAllListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return VideoReels.objects.filter(
            content_type=VideoReelsTypeChoices.REELS
        )

    pagination_class = DoctorProfileListPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['description', 'profile', 'content_type']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['id']


class UserReelsListAPIView(ListAPIView):
    serializer_class = VideoAllListSerializer
    permission_classes = [UserAllVideoReelsPermission]

    def get_queryset(self):
        profile = RoleValidate.get_profile_user(self.request)
        return not VideoReels.objects.filter(
            profile_content_type=ContentType.objects.get_for_model(profile),
            profile_obj_id=profile.id,
            content_type=VideoReelsTypeChoices.REELS
        )


class VideoReelsAddViewAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, content_id):
        try:
            video = VideoReels.objects.get(id=content_id)
        except VideoReels.DoesNotExist:
            return CustomResponse.error_response(message="Video topilmadi", code=status.HTTP_404_NOT_FOUND)

        profile = RoleValidate.get_profile_user(request)
        ct = ContentType.objects.get_for_model(profile)

        obj, created = VideoReelsView.objects.get_or_create(
            content=video,
            profile_content_type=ct,
            profile_obj_id=profile.id
        )

        return CustomResponse.success_response(
            message="Video muvaffaqiyatli ko'rildi"
        )
