from rest_framework import serializers

from apps.doctor_application.models import DoctorApplication, DoctorApplicationChoices
from apps.users.serializers.user_detail import UserListSerializer
from apps.utils.CustomValidationError import CustomValidationError
from django.utils.translation import gettext_lazy as _


class AdminDoctorApplicationListSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)

    class Meta:
        model = DoctorApplication
        fields = ['id', 'user', 'image', 'region', 'district', 'address', 'full_name', 'birth_date', 'gender',
                  'passport',
                  'experience_year', 'passport_image', 'passport_image2', 'diplom_image', 'bio', 'status', 'created_at',
                  'term']


class AdminDoctorApplicationUpdateSerializer(serializers.Serializer):
    term = serializers.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M'], format='%Y-%m-%dT%H:%M:%SZ', )
    status = serializers.ChoiceField(choices=DoctorApplicationChoices.choices)

    def validate(self, attrs):
        term = attrs.get('term', None)
        if term is None:
            raise CustomValidationError(detail=_("Shikorlik muddati tugash sanasi aniqlanmadi"))
        status = attrs.get('status', None)
        if status is None:
            raise CustomValidationError(
                detail=_("Status topilmadi")
            )
        return attrs
