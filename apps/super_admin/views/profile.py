from drf_spectacular.utils import OpenApiParameter, extend_schema
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


@extend_schema(
    parameters=[
        OpenApiParameter(
            name='search',
            description='public_id, full_name, username',
            required=False,
            type=str
        ),
        OpenApiParameter(
            name='ordering',
            description='created_at, updated_at, full_name',
            required=False,
            type=str
        )
    ],
    summary='🔐 admin uchun'
)
class AdminDoctorProfileListAPIView(ListAPIView):
    serializer_class = AdminDoctorProfileListSerializer
    permission_classes = [AdminPermission]
    queryset = DoctorProfile.objects.select_related("user")
    pagination_class = AdminListPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_private']
    filterset_class = AdminDoctorProfileListFilter
    search_fields = ['username', 'user__full_name', 'public_id']
    ordering_fields = ['created_at', 'updated_at', 'user__full_name']
    ordering = ['id']


@extend_schema(summary='🔐 admin uchun')
class AdminDoctorProfileRetrieveAPIView(RetrieveAPIView):
    serializer_class = DoctorProfileSerializer
    permission_classes = [AdminPermission]
    lookup_field = 'public_id'

    def get_queryset(self):
        return DoctorProfile.objects.filter(status=True, public_id=self.kwargs.get('public_id')).first()

    def retrieve(self, request, *args, **kwargs):
        public_id = kwargs.get('public_id', None)
        if public_id is None:
            return CustomResponse.error_response(
                message="Public id topilmadi"
            )
        data = self.get_queryset()
        if not data:
            return CustomResponse.error_response(
                message="Shifokor topilmadi"
            )
        serializer = self.serializer_class(instance=data)
        return CustomResponse.success_response(
            data=serializer.data
        )


@extend_schema(
    parameters=[
        OpenApiParameter(
            name='search',
            description='public_id, full_name, slug',
            required=False,
            type=str
        ),
        OpenApiParameter(
            name='ordering',
            description='created_at, updated_at, full_name',
            required=False,
            type=str
        )
    ],
    summary='🔐 admin uchun'
)
class AdminPatientProfileListAPIView(ListAPIView):
    serializer_class = AdminPatientProfileListSerializer
    permission_classes = [AdminPermission]
    queryset = PatientProfile.objects.select_related('user').prefetch_related('patient_address')
    pagination_class = AdminListPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status']
    filterset_class = AdminPatientProfileListFilter
    search_fields = ['public_id', 'user__full_name', 'slug']
    ordering_fields = ['created_at', 'updated_at', 'user__full_name']
    ordering = ['id']

@extend_schema(summary='🔐 admin uchun')
class AdminPatientProfileRetrieveAPIView(RetrieveAPIView):
    permission_classes = [AdminPermission]
    serializer_class = AdminPatientProfileListSerializer
    lookup_field = 'public_id'

    def get_queryset(self):
        return PatientProfile.objects.filter(status=True, public_id=self.kwargs.get('public_id')).first()

    def retrieve(self, request, *args, **kwargs):
        public_id = kwargs.get('public_id', None)
        if public_id is None:
            return CustomResponse.error_response(
                message="Public id topilmadi"
            )
        data = self.get_queryset()
        if not data:
            return CustomResponse.error_response(
                message="Bemor topilmadi"
            )
        serializer = self.serializer_class(instance=data)
        return CustomResponse.success_response(
            data=serializer.data
        )
