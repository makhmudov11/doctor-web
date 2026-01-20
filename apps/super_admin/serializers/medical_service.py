from rest_framework import serializers

from apps.order.models import MedicalService


class AdminMedicalServiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalService
        fields = '__all__'


class AdminMedicalServiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalService
        fields = ['name', 'price', 'description', 'units', 'code',
                  'package_code', 'vat_percent', 'status', 'created_at']
        extra_kwargs = {
            "description": {"required": False},
            "name": {"required": True},
            "price": {"required": True},
            "units": {"required": True},
            "code": {"required": True},
            "package_code": {"required": True},
            "vat_percent": {"required": True},
            'status': {"read_only": True},
            'created_at': {"read_only": True},
        }
