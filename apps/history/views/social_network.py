from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from apps.service.models import SocialNetwork

from ..serializers.social_network import SocialNetworkListSerializer
from ...utils.CustomResponse import CustomResponse
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

@extend_schema(summary='🔐 login qilgan hamma uchun')
class SocialNetworkListAPIView(ListAPIView):
    serializer_class = SocialNetworkListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SocialNetwork.objects.filter(status=True)

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
@extend_schema(summary='🔐 login bolgan hamma uchun')
class SocialNetworkDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, social_id):
        if not social_id:
            return CustomResponse.error_response(
                message=_("Ijtimoiy tarmoq id kelishi shart")
            )

        try:
            data = SocialNetwork.objects.get(id=social_id, status=True)
        except SocialNetwork.DoesNotExist:
            return CustomResponse.error_response(
                message=_("Ijtimoy tarmoq topilmadi"),
                code=status.HTTP_404_NOT_FOUND
            )
        serializer = SocialNetworkListSerializer(data)
        return CustomResponse.success_response(
            data=serializer.data
        )