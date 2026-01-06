from rest_framework import serializers

from apps.history.models import Address
from apps.profile.serializers.profiles import PatientProfileSerializer
from apps.utils.CustomValidationError import CustomValidationError
from django.utils.translation import gettext_lazy as _


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ['patient']


class AddressFullDataSerializer(serializers.ModelSerializer):
    patient = PatientProfileSerializer(read_only=True)

    class Meta:
        model = Address
        fields = [
            'id', 'patient', 'region', 'district', 'street', 'home', 'building_number', 'floor', 'address_type',
            'longitude', 'latitude', 'entrance', 'status', 'created_at'
        ]


class AddressCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ['region', 'district', 'street', 'home',
                  'longitude', 'latitude', 'entrance', 'floor', 'building_number', 'notes', 'address_type']
        extra_kwargs = {
            "longitude": {"required": True},
            "latitude": {"required": True},
            "region": {"required": True},
            "district": {"required": True},
            "street": {"required": True},
            "entrance": {"required": False},
            "floor": {"required": False},
            "building_number": {"required": True},
            "notes": {"required": False},
            "address_type": {"required": False},
            "home": {"required": False},
        }

    def validate(self, attrs):
        required_fields = {
            "region": "Shahar kelishi shart",
            "district": "Tuman nomi kelishi shart",
            "street": "Mahalla nomi kelishi shart",
            "building_number": "Dom raqami kelishi shart",
            "longitude": "Longitude kelishi shart",
            "latitude": "Latitude kelishi shart",
        }

        for field, message in required_fields.items():
            if not attrs.get(field):
                raise CustomValidationError(detail=_(message))

        return attrs
