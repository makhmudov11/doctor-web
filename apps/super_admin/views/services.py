from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils.translation import gettext_lazy as _

from apps.banner.models import Banner
from apps.service.models import Service, SocialNetwork
from apps.super_admin.paginations.profile import AdminListPagination
from apps.super_admin.permissions.users import AdminPermission
from apps.super_admin.serializers.services import AdminBannerCreateSerializer, AdminServiceCreateSerializer, \
    AdminBannerAllSerializer, AdminServiceAllSerializer, AdminBannerDetailUpdateSerializer, \
    AdminSocialNetworkUpdateSerializer
from apps.utils.CustomResponse import CustomResponse
from apps.history.serializers.social_network import SocialNetworkListSerializer
from apps.utils.CustomValidationError import CustomValidationError


@extend_schema(summary='🔐 admin uchun')
class AdminBannerCreateAPIView(CreateAPIView):
    serializer_class = AdminBannerCreateSerializer
    permission_classes = [AdminPermission]
    queryset = Banner.objects.all()
    parser_classes = [MultiPartParser, FormParser]

@extend_schema(summary='🔐 admin uchun')
class AdminServiceCreateAPIView(CreateAPIView):
    serializer_class = AdminServiceCreateSerializer
    permission_classes = [AdminPermission]
    queryset = Service.objects.all()
    parser_classes = [MultiPartParser, FormParser]

@extend_schema(summary='🔐 admin uchun')
class AdminBannerRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [AdminPermission]
    queryset = Banner.objects.all()
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return AdminBannerDetailUpdateSerializer
        return AdminBannerAllSerializer

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return CustomResponse.success_response(
                message=_("Banner topildi"),
                data=serializer.data
            )
        except Exception:
            return CustomResponse.error_response(
                message=_("Banner topilmadi"),
                code=status.HTTP_404_NOT_FOUND
            )

@extend_schema(summary='🔐 admin uchun')
class AdminServicesRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [AdminPermission]
    queryset = Service.objects.all()
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return AdminServiceCreateSerializer
        return AdminServiceAllSerializer

@extend_schema(
    parameters=[
        OpenApiParameter(
            name='search',
            description='title, description, _type, status',
            required=False,
            type=str
        ),
        OpenApiParameter(
            name='ordering',
            description='created_at, updated_at',
            required=False,
            type=str
        )
    ],
    summary='🔐 admin uchun'
)
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


@extend_schema(
    parameters=[
        OpenApiParameter(
            name='search',
            description='title, description, status',
            required=False,
            type=str
        ),
        OpenApiParameter(
            name='ordering',
            description='created_at, updated_at',
            required=False,
            type=str
        )
    ],
    summary='🔐 admin uchun'
)

class ServiceListAPIView(ListAPIView):
    """
    Servislar listi
    """
    serializer_class = AdminServiceAllSerializer
    permission_classes = [AdminPermission]
    pagination_class = AdminListPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'description', 'status']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    queryset = Service.objects.all()

@extend_schema(
    parameters=[
        OpenApiParameter(
            name='search',
            description='title, description, link',
            required=False,
            type=str
        ),
        OpenApiParameter(
            name='ordering',
            description='created_at, updated_at, status',
            required=False,
            type=str
        )
    ],
    summary='🔐 admin uchun'
)
class AdminSocialNetworkListAPIView(ListAPIView):
    serializer_class = SocialNetworkListSerializer
    permission_classes = [AdminPermission]
    queryset = SocialNetwork.objects.all()
    pagination_class = AdminListPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'description', 'link']
    ordering_fields = ['created_at', 'updated_at', 'status']
    ordering = ['-created_at']


    def list(self, request, *args, **kwargs):
        data = self.get_queryset()
        if not data.exists():
            return CustomResponse.error_response(
                message=_("Malumot topilmadi"),
                code=status.HTTP_204_NO_CONTENT
            )
        serializer = self.serializer_class(instance=data, many=True)
        return CustomResponse.success_response(
            data=serializer.data
        )




@extend_schema(summary='🔐 admin uchun')
class AdminSocialNetworkDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [AdminPermission]
    queryset = SocialNetwork.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'social_id'
    parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return AdminSocialNetworkUpdateSerializer
        return SocialNetworkListSerializer

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise CustomValidationError(_("Ijtimoiy tarmoq topilmadi"), code=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CustomResponse.success_response(data=serializer.data)

    def update(self, request, *args, **kwargs):
        partial = self.request.method == 'PATCH'
        instance = self.get_object()

        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return CustomResponse.success_response(data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = False
        instance.save(update_fields=['status'])

        return CustomResponse.success_response(
            message=_("Ijtimoiy tarmoq o‘chirildi"),
            code=status.HTTP_204_NO_CONTENT
        )

