from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView

from apps.banner.models import Banner
from apps.service.models import Service
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