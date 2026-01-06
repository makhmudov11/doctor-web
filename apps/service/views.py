from django.utils.translation import gettext_lazy as _
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.service.models import Service
from apps.service.serializers import ServiceListSerializer
from apps.utils.CustomResponse import CustomResponse
from drf_spectacular.utils import extend_schema

@extend_schema(summary='🔐 login qilgan hamma uchun')
class ServiceListAPIView(ListAPIView):
    """
    Servislar listi
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ServiceListSerializer

    def get_queryset(self):
        return Service.objects.filter(
            status=True
        )

    def list(self, request, *args, **kwargs):
        services = self.get_queryset()
        if not services.exists():
            empty_data = [{field: None for field in self.serializer_class().fields}]
            return CustomResponse.error_response(
                message=_("Servislar topilmadi"),
                data=empty_data
            )
        serializer = self.get_serializer(services, many=True)
        return CustomResponse.success_response(
            data=serializer.data
        )
@extend_schema(summary='🔐 login qilgan hamma uchun')
class ServiceDetailAPIView(APIView):
    """
    Servis detail
    """
    serializer_class = ServiceListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, service_id):
        empty_data = {field: None for field in self.serializer_class().fields}
        if not service_id:
            return CustomResponse.error_response(
                message=_("Servis id topilmadi"),
                data=empty_data
            )
        try:
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            return CustomResponse.error_response(
                message=_("Servis topilmadi"),
                data=empty_data
            )
        serializer = self.serializer_class(instance=service).data

        if serializer.get('image'):
            serializer['image'] = request.build_absolute_uri(service.image.url)
        return CustomResponse.success_response(
            data=serializer
        )