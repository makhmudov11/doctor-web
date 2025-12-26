from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.profile.choices import FollowChoices
from apps.profile.doctor.models import DoctorProfile
from apps.profile.doctor.serializers import DoctorProfileSerializer
from apps.profile.follow.models import Follow
from apps.profile.patient.models import PatientProfile
from apps.profile.patient.permission import PatientPermission
from apps.profile.patient.serializers import PatientFollowUserSerializer, \
    PatientUnFollowUserSerializer, PatientProfileSerializer
from apps.utils.CustomResponse import CustomResponse


class PatientFollowCountAPIView(APIView):
    permission_classes = [PatientPermission]

    def get(self, request):

        try:
            profile = request.user.patient_profile
        except Exception as e:
            profile = None

        if profile is None:
            return CustomResponse.error_response(
                message='Bemorga tegishli profile topilmadi'
            )
        try:

            return CustomResponse.success_response(
                data={"following_count": profile.following_count}
            )
        except Exception as e:
            return CustomResponse.error_response(
                message='Malumot olishda xatolik',
            )


class PatientFollowListAPIView(ListAPIView):
    permission_classes = [PatientPermission]

    def get_queryset(self):
        try:
            profile = self.request.user.patient_profile
        except Exception as e:
            profile = None
        if profile is None:
            return CustomResponse.error_response(
                message='Bemorga tegishli profile topilmadi'
            )
        qs = Follow.objects.filter(
            profile_content_type=ContentType.objects.get_for_model(profile),
            profile_obj_id=profile.id,
            status=FollowChoices.FOLLOW
        )
        if not qs:
            return CustomResponse.error_response(
                message='Userga tegishlo followlar mavjud emas'
            )
        return qs

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if isinstance(queryset, Response):
            return queryset


        follows = []
        for qs in queryset:
            profile = qs.profile
            follows.append(qs.following)

        return Response(
            {"profile": PatientProfileSerializer(profile).data,
             "follows": DoctorProfileSerializer(follows, many=True).data
             }
        )


class PatientFollowUserCreateAPIView(CreateAPIView):
    serializer_class = PatientFollowUserSerializer
    permission_classes = [PatientPermission]
    queryset = Follow.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            patient_profile = self.request.user.patient_profile
        except Exception as e:
            patient_profile = None

        if patient_profile is None:
            return CustomResponse.error_response(
                message='Foydalanuvchiga tegishli profile topilmadi'
            )

        profile_public_id = kwargs.get('profile_public_id', None)
        serializer = self.serializer_class(data=request.data,
                                           context={'profile_public_id': profile_public_id})
        serializer.is_valid(raise_exception=True)
        doctor_profile = DoctorProfile.objects.filter(
            public_id=profile_public_id
        ).first()
        if not doctor_profile:
            return CustomResponse.error_response(
                message=f"{profile_public_id} lik shifokor topilmadi"
            )
        try:
            with transaction.atomic():
                follow_obj, created = Follow.objects.get_or_create(
                    profile_content_type=ContentType.objects.get_for_model(patient_profile),
                    profile_obj_id=patient_profile.id,
                    following=doctor_profile
                )

                if not created:
                    if follow_obj.status == FollowChoices.UNFOLLOW:
                        follow_obj.status = FollowChoices.FOLLOW
                        follow_obj.save(update_fields=['status'])
                    else:
                        return CustomResponse.error_response(
                            message='Siz avval follow qilgansiz'
                        )
                data = self.serializer_class(instance=follow_obj).data
                return CustomResponse.success_response(
                    message='Follow muvaffaqiyatli amalga oshirildi',
                    data=data,
                    code=status.HTTP_201_CREATED
                )
        except Exception as e:
            return CustomResponse.error_response(
                message=f'Malumot saqlashda xatolik: {str(e)}'
            )


class PatientUnfollowUserAPIView(APIView):
    serializer_class = PatientUnFollowUserSerializer
    permission_classes = [PatientPermission]

    def post(self, request, *args, **kwargs):
        try:
            patient_profile = self.request.user.patient_profile
        except Exception as e:
            patient_profile = None
        if patient_profile is None:
            raise CustomResponse.error_response(
                message=f'Userga tegishli profile mavjud emas',
                code=status.HTTP_404_NOT_FOUND
            )

        profile_public_id = kwargs.get('profile_public_id', None)
        serializer = self.serializer_class(data=request.data,
                                           context={'profile_public_id': profile_public_id})
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                follow_obj = Follow.objects.get(
                    profile_content_type=ContentType.objects.get_for_model(patient_profile),
                    profile_obj_id=patient_profile.id,
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
