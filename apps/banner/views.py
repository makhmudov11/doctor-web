from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.banner.models import Banner
from apps.banner.serializers import BannerListSerializer
from apps.utils.CustomResponse import CustomResponse
from django.utils.translation import gettext_lazy as _

@extend_schema(summary='🔐 login qilgan hamma uchun')
class BannerListAPIView(ListAPIView):
    """
        Banner listini olish
    """
    serializer_class = BannerListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Banner.objects.filter(
            status=True
        )

    def list(self, request, *args, **kwargs):
        banners = self.get_queryset()
        if not banners.exists():
            empty_data = [{field: None for field in self.serializer_class().fields}]
            return CustomResponse.error_response(
                message=_("Banner topilmadi"),
                data=empty_data
            )
        serializer = self.get_serializer(banners, many=True)
        return CustomResponse.success_response(
            data=serializer.data
        )
@extend_schema(summary='🔐 login qilgan hamma uchun')
class BannerDetailAPIView(APIView):
    """
    Banner detail
    """
    serializer_class = BannerListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, banner_id):
        empty_data = {field: None for field in self.serializer_class().fields}
        if not banner_id:
            return CustomResponse.error_response(
                message=_("Banner id topilmadi"),
                data=empty_data
            )
        try:
            banner = Banner.objects.get(id=banner_id)
        except Banner.DoesNotExist:
            return CustomResponse.error_response(
                message=_("Banner topilmadi"),
                data=empty_data
            )
        serializer = self.serializer_class(instance=banner).data

        if serializer.get('image'):
            serializer['image'] = request.build_absolute_uri(banner.image.url)
        return CustomResponse.success_response(
            data=serializer.data
        )