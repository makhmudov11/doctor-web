from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.profile.choices import FollowChoices
from apps.profile.doctor.models import DoctorProfile
from apps.profile.follow.models import Follow
from apps.profile.patient.models import PatientProfile
from apps.profile.patient.permission import PatientPermission
from apps.profile.patient.serializers import PatientFollowListSerializer, PatientFollowUserSerializer
from apps.utils.CustomResponse import CustomResponse


class PatientFollowCountAPIView(APIView):
    permission_classes = [PatientPermission]
    def get(self, request):
        profile = request.user.patient_profile
        if not profile:
            return CustomResponse.error_response(
                message='Bemorga tegishli profile topilmadi'
            )
        try:
            return Follow.get_follow_count(profile=profile)
        except Exception as e:
            return CustomResponse.error_response(
                message='Malumot olishda xatolik',
            )


class PatientFollowListAPIView(ListAPIView):
    serializer_class = PatientFollowListSerializer
    permission_classes = [PatientPermission]

    def get_queryset(self):
        try:
            profile = self.request.user.patient_profile
        except Exception as e:
            return CustomResponse.error_response(
                message='Bemorga tegishli profile topilmadi'
            )
        return Follow.objects.filter(
            profile_content_type=ContentType.objects.get_for_model(PatientProfile),
            profile_obj_id=profile.id,
            status=FollowChoices.FOLLOW
        )


class PatientFollowUserCreateAPIView(CreateAPIView):
    serializer_class = PatientFollowUserSerializer
    permission_classes = [PatientPermission]
    queryset = Follow.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile_public_id = serializer.validated_data.get('profile_public_id').strip()
        doctor_profile = DoctorProfile.objects.filter(
            public_id=int(profile_public_id)
        ).first()
        if not doctor_profile:
            return CustomResponse.error_response(
                message=f"{profile_public_id} lik shifokor topilmadi"
            )
        patient_profile = getattr(request.user, 'patient_profile', None)
        if patient_profile is None:
            return CustomResponse.error_response(
                message='Foydalnuvchiga tegishli profile topilmadi'
            )
        try:
            follow_obj = Follow.objects.create(
                profile_content_type=ContentType.objects.get_for_model(PatientProfile),
                profile_obj_id=patient_profile.id,
                following=doctor_profile
            )

            serializer.save()
            data = PatientFollowListSerializer(instance=follow_obj).data
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
    serializer_class = PatientFollowUserSerializer
    permission_classes = [PatientPermission]
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile_public_id = int(serializer.validated_data.get('profile_public_id').strip())
        patient_profile = getattr(request.user, 'patient_profile', None)
        if patient_profile is None:
            return CustomResponse.error_response(
                message='Foydalanuvchiga tegishli profile mavjud emas',
                code=status.HTTP_404_NOT_FOUND
            )

        try:
            with transaction.atomic():
                follow_obj = Follow.objects.get(
                    profile_content_type=ContentType.objects.get_for_model(PatientProfile),
                    profile_obj_id=patient_profile.id,
                    following=DoctorProfile.objects.get(public_id=profile_public_id),
                    status=FollowChoices.FOLLOW
                )

                follow_obj.status = FollowChoices.UNFOLLOW
                follow_obj.save(update_fields=['status'])

                patient_profile.following_count -= 1
                patient_profile.save(update_fields=['following_count'])

            return CustomResponse.success_response(
                message='Unfollow muvaffaqiyatli bajarildi'
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