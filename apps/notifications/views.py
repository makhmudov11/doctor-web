from django.utils import timezone
from drf_spectacular.utils import extend_schema
from firebase_admin import messaging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.notifications.models import FCMDevice, Notification
from apps.notifications.serializers import FCMDeviceCreateSerializer, FCMDeviceLogoutSerializer, \
    NotificationListSerializer
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


@extend_schema(summary="🔐 login bo'lganlar uchun")
class NotificationReadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, notification_id):
        if not notification_id:
            return CustomResponse.error_response(
                message=_("Xabar raqami kelishi shart")
            )
        try:
            obj = Notification.objects.get(
                id=notification_id,
                device__user=request.user
            )
        except Notification.DoesNotExist:
            return CustomResponse.error_response(
                message=_("Xabar topilmadi"),
                code=status.HTTP_404_NOT_FOUND
            )

        serializer = NotificationListSerializer(instance=obj)
        if obj.is_read:
            return CustomResponse.success_response(
                data=serializer.data,
                message="Xabar avval o‘qilgan"
            )

        obj.is_read = True
        obj.read_at = timezone.now()
        obj.save(update_fields=["is_read", "read_at"])

        return CustomResponse.success_response(
            data=serializer.data,
            message="Xabar o‘qildi"
        )


@extend_schema(summary="🔐 login bo'lganlar uchun")
class NotificationDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, notification_id):
        if not notification_id:
            return CustomResponse.error_response(
                message=_("Xabar raqami kelishi shart")
            )
        try:
            obj = Notification.objects.get(
                id=notification_id,
                device__user=request.user
            )
        except Notification.DoesNotExist:
            return CustomResponse.error_response(
                message=_("Xabar topilmadi"),
                code=status.HTTP_404_NOT_FOUND
            )
        obj.deleted_at = timezone.now()
        obj.save(update_fields=['deleted_at'])
        return CustomResponse.success_response(
            message=_("Muvaffaqiyatli o'chirildi"),
            code=status.HTTP_200_OK
        )


@extend_schema(summary="🔐 login bo'lganlar uchun")
class NotificationListAPIView(APIView):
    serializer_class = NotificationListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        obj = Notification.objects.filter(
            device__user=request.user,
            device__is_active=True,
            deleted_at=None
        ).order_by('-created_at')
        serializer = self.serializer_class(instance=obj, many=True)
        return CustomResponse.success_response(
            data=serializer.data
        )


@extend_schema(summary="🔐 login bo'lganlar uchun")
class NotificationDetailAPIView(APIView):
    serializer_class = NotificationListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, notification_id):
        if not notification_id:
            return CustomResponse.error_response(
                message=_("Xabar raqami kelishi shart")
            )
        try:
            obj = Notification.objects.get(
                id=notification_id,
                device__user=request.user
            )
        except Notification.DoesNotExist:
            return CustomResponse.error_response(
                message=_("Xabar topilmadi"),
                code=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer_class(instance=obj)
        return CustomResponse.success_response(
            data=serializer.data
        )
