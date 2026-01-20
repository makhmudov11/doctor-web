from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, CreateAPIView

from apps.order.models import MedicalService
from apps.super_admin.filters.medical_service import AdminMedicalServiceListFilter
from apps.super_admin.paginations.profile import AdminListPagination
from apps.super_admin.permissions.users import AdminPermission
from apps.super_admin.serializers.medical_service import AdminMedicalServiceListSerializer, AdminMedicalServiceCreateSerializer
@extend_schema(
    parameters=[
        OpenApiParameter(
            name='search',
            description='title, description, code, units, package_code, price',
            required=False,
            type=str
        ),
        OpenApiParameter(
            name='ordering',
            description='created_at, updated_at, status, price',
            required=False,
            type=str
        )
    ],
    summary='🔐 admin uchun'
)
class AdminMedicalServiceListAPIVew(ListAPIView):
    serializer_class = AdminMedicalServiceListSerializer
    permission_classes = [AdminPermission]
    queryset = MedicalService.objects.all()
    pagination_class = AdminListPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status']
    filterset_class = AdminMedicalServiceListFilter
    search_fields = ['title', 'description', 'code', 'units', 'package_code', 'price']
    ordering_fields = ['created_at', 'updated_at', 'status', 'price']
    ordering = ['created_at',]

@extend_schema(summary='🔐 admin uchun')
class AdminMedicalServiceCreateAPIView(CreateAPIView):
    serializer_class = AdminMedicalServiceCreateSerializer
    permission_classes = [AdminPermission]
    queryset = MedicalService.objects.all()