from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView

from apps.profile.models import DoctorProfile, Story, StoryView
from apps.profile.permission import IsDoctor, DoctorStoryPermission
from apps.profile.serializers.stories import UserStoryCreateSerializer, UserActiveStorySerializer, \
    UserStoryListSerializer
from apps.utils.CustomResponse import CustomResponse
from apps.utils.role_validate import RoleValidate


class UserStoryCreateAPIView(CreateAPIView):
    serializer_class = UserStoryCreateSerializer
    permission_classes = [IsDoctor]
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):

        try:
            profile = RoleValidate.get_role_model(request=request).objects.get(user=self.request.user)
        except Exception as e:
            return CustomResponse.error_response(message='Foydalanuvchiga tegishli profil mavjud emas')
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        story = serializer.save(profile=profile)
        full_data = self.get_serializer(story).data
        return CustomResponse.success_response(message='Storis muvaffaqiyatli yaratildi', data=full_data,
                                               code=HTTP_201_CREATED)


class UserActiveStoryListAPIView(ListAPIView):
    permission_classes = [DoctorStoryPermission]

    def get_queryset(self):
        return Story.objects.filter(
            expires_at__gte=timezone.now(),
            profile__user=self.request.user,
            status=False
        )

    def list(self, request, *args, **kwargs):
        print(request.user.is_authenticated)
        profile = RoleValidate.get_profile_user(request=request)
        stories = self.get_queryset()
        serializer = UserActiveStorySerializer({
            "profile": profile,
            "stories": stories
        }, context={"request": request})
        return Response(serializer.data)


class StoryMarkViewedAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, story_id):
        try:
            story_obj = Story.objects.get(id=story_id, status=False)
            profile = RoleValidate.get_profile_user(request=request)
            if story_obj.profile == profile:
                return CustomResponse.error_response(
                    message="O'zini storyini ko'rish mumkin lekin ko'rishlar soni oshmaydi"
                )
        except Story.DoesNotExist:
            return CustomResponse.error_response(
                message="Story topilmadi"
            )
        except Exception as e:
            return CustomResponse.error_response(
                message=f"Profile topilmadi: {str(e)}"
            )

        try:
            with transaction.atomic():
                stoy_view_obj, created = StoryView.objects.get_or_create(
                    story=story_obj,
                    profile_content_type=ContentType.objects.get_for_model(profile),
                    profile_obj_id=profile.id,
                )
                if not created:
                    return CustomResponse.error_response(
                        message="Siz ushbu storisni avval avval ko'rilgan"
                    )
                return CustomResponse.success_response(
                    message="Ko'rish muvaffaqiyatli bajarildi"
                )
        except Exception as e:
            return CustomResponse.error_response(
                message=f"Story saqlashda xatolik: {str(e)}"
            )


class UserStoryDeleteAPIView(DestroyAPIView):
    permission_classes = [DoctorStoryPermission]

    def destroy(self, request, *args, **kwargs):
        story_id = kwargs.get('story_id', None)
        if story_id is None:
            return CustomResponse.error_response(
                message="Storis id kelishi shart"
            )
        if not isinstance(story_id, int):
            return CustomResponse.error_response(
                message="Story id son bolishi kerak"
            )
        profile = RoleValidate.get_profile_user(request=request)
        print(profile)
        try:
            story_obj = Story.objects.get(id=story_id, profile=profile, status=False)
        except Story.DoesNotExist:
            return CustomResponse.error_response(
                message="Storis mavjud emas"
            )
        self.perform_destroy(instance=story_obj)
        return CustomResponse.success_response(
            message="Storis muvaffaqiyatli o'chirildi",
            code=status.HTTP_204_NO_CONTENT
        )


class UserStoryViewedAllListAPIView(ListAPIView):
    permission_classes = [IsDoctor]
    serializer_class = UserStoryListSerializer

    def get_queryset(self):
        profile = RoleValidate.get_profile_user(self.request)
        story_id = self.request.GET.get('story_id', None)
        if story_id is None or not isinstance(story_id, int):
            raise CustomResponse.error_response(
                message='Story id kelishi shart'
            )
        qs = StoryView.objects.filter(
            story__id=story_id,
            story__profile=profile,
            story__status=False
        )
        if not qs.exists():
            raise CustomResponse.error_response(
                message="Ko'rilganlar topilmadi"
            )
        return qs

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        story_id = kwargs.get('story_id')
        try:
            story = Story.objects.get(id=story_id)
        except Story.DoesNotExist:
            return CustomResponse.error_response(
                message="Storis topilmadi"
            )
        story_serializer = UserStoryListSerializer(instance=story,
                                                   context={'request': request})
        story_viewed_serializer = self.serializer_class(instance=qs,
                                                        context={'request': request})
        return CustomResponse.success_response(
            data={
                "story" : story_serializer.data,
                "story_view" : story_viewed_serializer.data
            }
        )