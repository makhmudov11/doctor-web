from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from apps.doctor_application.models import DoctorApplication
from apps.super_admin.filters.doctor_application import AdminDoctorApplicationListFilter
from apps.super_admin.paginations.profile import AdminListPagination
from apps.super_admin.permissions.users import AdminPermission
from apps.super_admin.serializers.doctor_application import AdminDoctorApplicationListSerializer, \
    AdminDoctorApplicationUpdateSerializer
from apps.utils.CustomResponse import CustomResponse
from django.utils.translation import gettext_lazy as _


@extend_schema(
    parameters=[
        OpenApiParameter(
            name='search',
            description='address, region, speciality, gender, district',
            required=False,
            type=str
        ),
        OpenApiParameter(
            name='ordering',
            description='created_at, updated_at, status, district, gender',
            required=False,
            type=str
        )
    ],
    summary='🔐 admin uchun'
)
class AdminDoctorApplicationListAPIView(ListAPIView):
    serializer_class = AdminDoctorApplicationListSerializer
    permission_classes = [AdminPermission]
    queryset = DoctorApplication.objects.all()
    pagination_class = AdminListPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status']
    filterset_class = AdminDoctorApplicationListFilter
    search_fields = ['address', 'full_name', 'region', 'speciality', 'district', 'gender']
    ordering_fields = ['created_at', 'updated_at', 'status', 'district', 'gender']
    ordering = ['created_at']


class AdminDoctorApplicationDetailAPIView(APIView):
    serializer_class = AdminDoctorApplicationListSerializer
    permission_classes = [AdminPermission]

    def get(self, request, id):
        if not id:
            return CustomResponse.error_response(
                message=_("Ariza raqami topilmadi")
            )
        try:
            obj = DoctorApplication.objects.get(id=id)
        except DoctorApplication.DoesNotExist:
            return CustomResponse.error_response(
                message=_("Kiritilgan ariza raqami bo'yicha malumot topilmadi"),
                code=status.HTTP_404_NOT_FOUND
            )
        return CustomResponse.success_response(
            data=self.serializer_class(instance=obj).data
        )


class AdminDoctorApplicationUpdateAPIView(APIView):
    serializer_class = AdminDoctorApplicationUpdateSerializer
    permission_classes = [AdminPermission]

    def post(self, request, id):
        if not id:
            return CustomResponse.error_response(
                message=_("Ariza raqami topilmadi")
            )
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            obj = DoctorApplication.objects.get(id=id)
        except DoctorApplication.DoesNotExist:
            return CustomResponse.error_response(
                message=_("Ariza raqami bo'yicha malumot topilmadi"), code=status.HTTP_404_NOT_FOUND
            )

        term = serializer.validated_data.get('term')
        status = serializer.validated_data.get('status')

        obj.term = term
        obj.status = status
        obj.save(update_fields=['term', 'status'])
        return CustomResponse.success_response(
            message=_("O'zgartirish uvaffaqiyatli bajarildi"),
            data=AdminDoctorApplicationListSerializer(obj).data
        )
