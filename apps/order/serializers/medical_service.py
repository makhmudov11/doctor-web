from rest_framework import serializers

from apps.order.models import MedicalService


class OrderServiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalService
        fields = ['name', 'price']