from drf_spectacular.utils import extend_schema
from firebase_admin import messaging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.notifications.models import FCMDevice
from apps.notifications.serializers import FCMDeviceCreateSerializer, FCMDeviceLogoutSerializer
from apps.utils.CustomResponse import CustomResponse
from django.utils.translation import gettext_lazy as _


class Notifications:
    @staticmethod
    def send_notification(token, title, body, image_url=None, extra_data=None):
        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                    image=image_url
                ),
                data=extra_data or {},
                token=token
            )

            response = messaging.send(message)
            return CustomResponse.success_response(
                data={
                    "token": token, "response": response
                }
            )

        except Exception as e:
            return CustomResponse.error_response(
                message=_(f"Xabar yuborishda xatolik, {str(e)}"), code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(summary="🔐 login bo'lganlar uchun")
class FCMDeviceCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FCMDeviceCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data.get('fcm_token')
        device_type = serializer.validated_data.get('device_type', None)
        FCMDevice.objects.update_or_create(
            token=token,
            defaults={
                "user": request.user,
                "device_type": device_type
            }
        )
        return CustomResponse.success_response(
            message=_("Device token muvaffaqiyatli saqlandi")
        )


@extend_schema(summary="🔐 login bo'lganlar uchun")
class FCMDeviceLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FCMDeviceLogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data.get('fcm_token')

        obj = FCMDevice.objects.filter(
            user=request.user,
            token=token,
            is_active=True
        ).first()
        if not obj:
            return CustomResponse.error_response(
                message=_("Token bo'yicha qurilma topilmadi"),
                code=status.HTTP_404_NOT_FOUND
            )
        obj.is_active = False
        obj.save(update_fields=['is_active'])

        return CustomResponse.success_response(message=_("Device logout qilindi"))
