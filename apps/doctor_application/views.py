from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView

from apps.doctor_application.models import DoctorApplication, DoctorApplicationChoices
from apps.doctor_application.serializers import DoctorApplicationCreateSerializer, DoctorApplicationFullDataSerializer, \
    SuccessDoctorApplicationSerializer
from apps.utils.CustomResponse import CustomResponse


@extend_schema(summary='🔐 login qilgan hamma uchun')
class DoctorApplicationCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DoctorApplicationCreateSerializer
    queryset = DoctorApplication.objects.all()
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        application_data = DoctorApplication.objects.filter(user=request.user).order_by('-created_at').first()
        if application_data:
            if application_data.status == DoctorApplicationChoices.PENDING:
                return CustomResponse.error_response(
                    message=_("Sizda allaqachon tekshiruvdagi ariza mavjud")
                )
            elif application_data.status == DoctorApplicationChoices.APPROVED:
                return CustomResponse.error_response(
                    message=_("Sizda tasdiqlangan ariza mavjud, iltimos muddat tuagagandan so'ng urinib ko'ring")
                )
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        return CustomResponse.success_response(
            message=_("Shifokor arizasi muvaffaqiyatli qabul qilindi"),
            data=self.get_serializer(instance=obj).data,
            code=status.HTTP_201_CREATED
        )


@extend_schema(summary='🔐 login qilgan hamma uchun')
class DoctorApplicationDetailAPIView(APIView):
    serializer_class = DoctorApplicationFullDataSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        if not id:
            return CustomResponse.error_response(
                message=_("Ariza raqami topilmadi")
            )
        try:
            obj = DoctorApplication.objects.get(id=id, user=request.user)
        except DoctorApplication.DoesNotExist:
            return CustomResponse.error_response(
                message=_("Bunday raqamli ariza topilmadi"),
                code=status.HTTP_404_NOT_FOUND
            )
        return CustomResponse.success_response(
            data=self.serializer_class(instance=obj).data
        )


class SuccessDoctorApplicationAPIView(APIView):
    serializer_class = SuccessDoctorApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        obj = DoctorApplication.objects.filter(
            user=request.user
        ).order_by('-created_at').first()
        if not obj:
            return CustomResponse.error_response(
                message=_("Sizda ariza mavjud emas"),
                code=status.HTTP_404_NOT_FOUND
            )
        if obj.status != DoctorApplicationChoices.APPROVED:
            return CustomResponse.error_response(
                message=_("Hozirda sizga tegishli tasdiqlangan ariza mavjud emas"),
                code=status.HTTP_404_NOT_FOUND
            )
        return CustomResponse.success_response(
            message="Sizda tasdiqlangan ariza mavjud",
            data=self.serializer_class(instance=obj).data
        )
