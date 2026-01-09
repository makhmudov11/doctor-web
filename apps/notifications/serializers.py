from rest_framework import serializers

from apps.notifications.models import Notification
from apps.utils.CustomValidationError import CustomValidationError
from django.utils.translation import gettext_lazy as _


class FCMDeviceCreateSerializer(serializers.Serializer):
    fcm_token = serializers.CharField(max_length=200)
    device_type = serializers.CharField(max_length=50)

    def validate(self, attrs):
        fcm_token = attrs.get('fcm_token', None)
        if not fcm_token:
            raise CustomValidationError(
                detail=_("Token kelishi shart")
            )
        return attrs


class FCMDeviceLogoutSerializer(serializers.Serializer):
    fcm_token = serializers.CharField(max_length=200)

    def validate(self, attrs):
        fcm_token = attrs.get('fcm_token', None)
        if not fcm_token:
            raise CustomValidationError(
                detail=_("Token kelishi shart")
            )
        return attrs

class NotificationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'is_read', 'read_at', 'created_at', 'title', 'message', 'data']