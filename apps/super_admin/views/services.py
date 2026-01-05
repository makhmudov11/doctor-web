from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView

from apps.banner.models import Banner
from apps.service.models import Service
from apps.super_admin.paginations.profile import AdminListPagination
from apps.super_admin.permissions.users import AdminPermission
from apps.super_admin.serializers.services import AdminBannerCreateSerializer, AdminServiceCreateSerializer, \
    AdminBannerAllSerializer, AdminServiceAllSerializer


class AdminBannerCreateAPIView(CreateAPIView):
    serializer_class = AdminBannerCreateSerializer
    permission_classes = [AdminPermission]
    queryset = Banner.objects.all()


class AdminServiceCreateAPIView(CreateAPIView):
    serializer_class = AdminServiceCreateSerializer
    permission_classes = [AdminPermission]
    queryset = Service.objects.all()


class AdminBannerRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [AdminPermission]
    queryset = Banner.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return AdminBannerCreateSerializer
        return AdminBannerAllSerializer


class AdminServicesRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [AdminPermission]
    queryset = Service.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return AdminServiceCreateSerializer
        return AdminServiceAllSerializer



class AdminBannerListAPIView(ListAPIView):
    """
        Banner listini olish
    """
    serializer_class = AdminBannerAllSerializer
    permission_classes = [AdminPermission]
    pagination_class = AdminListPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'description', '_type', 'status']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    queryset = Banner.objects.all()


class ServiceListAPIView(ListAPIView):
    """
    Servislar listi
    """
    serializer_class = AdminServiceAllSerializer
    permission_classes = [AdminPermission]
    pagination_class = AdminListPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'descriptiom', 'status']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    queryset = Service.objects.all()