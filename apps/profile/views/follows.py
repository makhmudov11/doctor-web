from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.profile.choices import FollowChoices
from apps.profile.models import DoctorProfile, Follow
from apps.profile.permission import IsDoctor, IsPatient, UserFollowListPermission
from apps.profile.serializers.follows import UserFollowCreateSerializer, UserUnFollowUserSerializer, \
    UserFollowersListSerializer
from apps.profile.serializers.profiles import GET_ROLE_SERIALIZER, DoctorProfileSerializer
from apps.utils.CustomResponse import CustomResponse
from apps.utils.CustomValidationError import CustomValidationError
from apps.utils.role_validate import RoleValidate


class UserFollowListAPIView(ListAPIView):
    permission_classes = [UserFollowListPermission]

    def get_queryset(self):
        profile = RoleValidate.get_profile_user(request=self.request)

        qs = Follow.objects.filter(
            profile_content_type=ContentType.objects.get_for_model(profile),
            profile_obj_id=profile.id,
            status=FollowChoices.FOLLOW
        )
        if not qs.exists():
            raise CustomValidationError(
                detail=f'{self.request.user.full_name or '?'}ga tegishli followlar mavjud emas'
            )
        return qs

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        follows = []
        for qs in queryset:
            follows.append(qs.following)

        profile_serializer = GET_ROLE_SERIALIZER.get(RoleValidate.get_role(request))
        following_serializer = DoctorProfileSerializer(follows, many=True)
        return CustomResponse.success_response(
            data={
                "profile": profile_serializer(RoleValidate.get_profile_user(request)).data,
                "follows": following_serializer.data
            }
        )


class UserFollowCreateAPIView(CreateAPIView):
    serializer_class = UserFollowCreateSerializer
    permission_classes = [UserFollowListPermission]
    queryset = Follow.objects.all()

    def create(self, request, *args, **kwargs):
        profile = RoleValidate.get_profile_user(request=request)
        profile_public_id = kwargs.get('profile_public_id', None)
        serializer = self.serializer_class(data=request.data,
                                           context={'profile_public_id': profile_public_id,
                                                    "request": request}
                                           )
        serializer.is_valid(raise_exception=True)
        if profile_public_id == profile.public_id:
            return CustomResponse.error_response(
                message="O'z o'ziga follow qilish mumkin emas"
            )
        try:
            following_user = DoctorProfile.objects.get(
                public_id=profile_public_id
            )
        except DoctorProfile.DoesNotExist:
            return CustomResponse.error_response(
                message=f"{profile_public_id} lik shifokor topilmadi"
            )
        try:
            with transaction.atomic():
                follow_obj, created = Follow.objects.get_or_create(
                    profile_content_type=ContentType.objects.get_for_model(profile),
                    profile_obj_id=profile.id,
                    following=following_user
                )
                if not created:
                    if follow_obj.status == FollowChoices.UNFOLLOW:
                        follow_obj.status = FollowChoices.FOLLOW
                        follow_obj.save(update_fields=['status'])
                    else:
                        return CustomResponse.error_response(
                            message='Siz avval follow qilgansiz'
                        )
                data = self.serializer_class(instance=follow_obj, context={"request": request}).data
                return CustomResponse.success_response(
                    message='Follow muvaffaqiyatli amalga oshirildi',
                    data=data,
                    code=status.HTTP_201_CREATED
                )
        except Exception as e:
            return CustomResponse.error_response(
                message=f'Malumot saqlashda xatolik: {str(e)}'
            )


class UserUnfollowUserAPIView(APIView):
    serializer_class = UserUnFollowUserSerializer
    permission_classes = [UserFollowListPermission]

    def post(self, request, *args, **kwargs):
        profile = RoleValidate.get_profile_user(request)

        profile_public_id = kwargs.get('profile_public_id', None)
        serializer = self.serializer_class(data=request.data,
                                           context={'profile_public_id': profile_public_id})
        serializer.is_valid(raise_exception=True)
        if profile_public_id == profile.public_id:
            return CustomResponse.error_response(
                message="O'z o'zidan unfollow qilish mumkin emas"
            )
        try:
            with transaction.atomic():
                follow_obj = Follow.objects.get(
                    profile_content_type=ContentType.objects.get_for_model(profile),
                    profile_obj_id=profile.id,
                    following=DoctorProfile.objects.get(public_id=profile_public_id),
                    status=FollowChoices.FOLLOW
                )
                follow_obj.status = FollowChoices.UNFOLLOW
                follow_obj.save(update_fields=['status'])

                return CustomResponse.success_response(
                    message='Unfollow muvaffaqiyatli bajarildi',
                )
        except DoctorProfile.DoesNotExist:
            return CustomResponse.error_response(
                message=f"{profile_public_id} lik shifokor topilmadi",
                code=status.HTTP_404_NOT_FOUND
            )
        except Follow.DoesNotExist:
            return CustomResponse.error_response(
                message="Foydalanuvchi ushbu shifokorga follow qilmagan",
                code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return CustomResponse.error_response(
                message=f'Unfollow qilishda xatolik yuz berdi: {str(e)}',
                code=status.HTTP_400_BAD_REQUEST
            )


class UserFollowerListAPIView(ListAPIView):
    serializer_class = UserFollowersListSerializer
    permission_classes = [IsDoctor]

    def get_queryset(self):
        profile = RoleValidate.get_profile_user(self.request)
        qs = Follow.objects.filter(
            following=profile,
            status=FollowChoices.FOLLOW
        )
        if not qs.exists():
            raise CustomValidationError(
                detail="Userga tegishli followerslar mavjud emas"
            )
        return qs

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        followers = []
        for qs in queryset:
            followers.append(qs.profile)

        profile_serializer = GET_ROLE_SERIALIZER.get(RoleValidate.get_role(request))
        following_serializer = self.serializer_class(followers, many=True)
        return CustomResponse.success_response(
            data={
                "profile": profile_serializer(RoleValidate.get_profile_user(request)).data,
                "followers": following_serializer.data
            }
        )