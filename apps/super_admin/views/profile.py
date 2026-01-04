from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from apps.super_admin.filters.profile import AdminDoctorProfileListFilter, AdminPatientProfileListFilter
from apps.super_admin.serializers.profile import AdminDoctorProfileListSerializer, AdminDoctorProfileCreateSerializer, AdminDoctorProfileRetrieveUpdateDestroySerializer, AdminPatientProfileCreateSerializer, AdminPatientProfileListSerializer, AdminPatientProfileRetrieveUpdateDestroySerializer
from apps.super_admin.permissions.users import AdminPermission
from apps.profile.models import DoctorProfile, PatientProfile
from apps.super_admin.paginations.profile import AdminListPagination


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


class AdminDoctorProfileCreateAPIView(CreateAPIView):
    serializer_class = AdminDoctorProfileCreateSerializer
    permission_classes = [AdminPermission]
    queryset = DoctorProfile.objects.all()


class AdminDoctorProfileRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = AdminDoctorProfileRetrieveUpdateDestroySerializer
    permission_classes = [AdminPermission]
    queryset = DoctorProfile.objects.all()



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


class AdminPatientProfileCreateAPIView(CreateAPIView):
    serializer_class = AdminPatientProfileCreateSerializer
    permission_classes = [AdminPermission]
    queryset = PatientProfile.objects.all()


class AdminPatientProfileRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = AdminPatientProfileRetrieveUpdateDestroySerializer
    permission_classes = [AdminPermission]
    queryset = PatientProfile.objects.all()