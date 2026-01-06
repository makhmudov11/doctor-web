from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django_filters.rest_framework import DjangoFilterBackend

from apps.profile.serializers.profiles import DoctorProfileSerializer, PatientProfileSerializer
from apps.super_admin.filters.profile import AdminDoctorProfileListFilter, AdminPatientProfileListFilter
from apps.super_admin.serializers.profile import AdminDoctorProfileListSerializer, AdminPatientProfileListSerializer
from apps.super_admin.permissions.users import AdminPermission
from apps.profile.models import DoctorProfile, PatientProfile
from apps.super_admin.paginations.profile import AdminListPagination
from apps.utils.CustomResponse import CustomResponse
from django.utils.translation import gettext_lazy as _


class AdminDoctorProfileListAPIView(ListAPIView):
    serializer_class = AdminDoctorProfileListSerializer
    permission_classes = [AdminPermission]
    queryset = DoctorProfile.objects.select_related("user")
    pagination_class = AdminListPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_private']
    filterset_class = AdminDoctorProfileListFilter
    search_fields = ['username', 'user__full_name']
    ordering_fields = ['created_at', 'updated_at', 'full_name']
    ordering = ['id']


class AdminDoctorProfileRetrieveAPIView(RetrieveAPIView):
    serializer_class = DoctorProfileSerializer
    permission_classes = [AdminPermission]

    def get_queryset(self):
        public_id = self.kwargs.get('public_id', None)
        if public_id is None:
            return CustomResponse.error_response(
                message=_("Shifokor id kelishi shart")
            )
        try:
            return DoctorProfile.objects.get(id=public_id, status=True)
        except DoctorProfile.DoesNotExist:
            return CustomResponse.error_response(
                message=_("Shifokor profili topilmadi")
            )


class AdminPatientProfileListAPIView(ListAPIView):
    serializer_class = AdminPatientProfileListSerializer
    permission_classes = [AdminPermission]
    queryset = PatientProfile.objects.select_related("user")
    pagination_class = AdminListPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status']
    filterset_class = AdminPatientProfileListFilter
    search_fields = ['public_id', 'user__full_name', 'slug']
    ordering_fields = ['created_at', 'updated_at', 'full_name']
    ordering = ['id']


class AdminPatientProfileRetrieveAPIView(RetrieveAPIView):
    queryset = PatientProfile.objects.all()
    permission_classes = [AdminPermission]
    serializer_class = PatientProfileSerializer

    def get_queryset(self):
        public_id = self.kwargs.get('public_id', None)
        if public_id is None:
            return CustomResponse.error_response(
                message=_("Bemor id kelishi shart")
            )
        try:
            return PatientProfile.objects.get(id=public_id, status=True)
        except PatientProfile.DoesNotExist:
            return CustomResponse.error_response(
                message=_("Bemor profili topilmadi")
            )
