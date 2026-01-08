from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from apps.doctor_application.models import DoctorApplication
from apps.users.serializers.user_detail import UserListSerializer
from apps.utils.CustomValidationError import CustomValidationError


class DoctorApplicationFullDataSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)

    class Meta:
        model = DoctorApplication
        fields = ['id', 'user', 'image', 'region', 'district', 'address', 'full_name', 'birth_date', 'gender', 'passport',
                  'experience_year', 'passport_image', 'passport_image2', 'diplom_image', 'bio', 'status', 'created_at']




class DoctorApplicationCreateSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateField(
        input_formats=["%d.%m.%Y", "%d/%m/%Y"],
        required=True
    )
    user = UserListSerializer(read_only=True)

    class Meta:
        model = DoctorApplication
        fields = ['id', 'user', 'image', 'region', 'district', 'address', 'full_name', 'birth_date', 'gender',
                  'passport', 'experience_year', 'passport_image', 'passport_image2', 'diplom_image', 'bio',
                  'status', 'created_at']

        extra_kwargs = {
            'image': {'required': True},
            'region': {'required': True},
            'district': {'required': True},
            'address': {'required': True},
            'full_name': {'required': True},
            'experience_year': {'required': True},
            'gender': {'required': True},
            'passport': {'required': True},
            'passport_image': {'required': True},
            'passport_image2': {'required': True},
            'diplom_image': {'required': True},
            'bio': {'required': True},
            'status': {'read_only': True},
            'created_at': {'read_only': True},
            'id': {"read_only": True}
        }

    def create(self, validated_data):
        user = self.context['request'].user
        return DoctorApplication.objects.create(user=user, **validated_data)

    # def validate(self, attrs):
    #     image = attrs.get('image', None)
    #     if image is None:
    #         raise CustomValidationError(detail=_("Rasm kiritilishi shart"))
    #     region = attrs.get('region', None)
    #     if region is None:
    #         raise CustomValidationError(detail=_("Shahar kiritilishi shart"))
    #     full_name = attrs.get('full_name', None)
    #     if full_name is None:
    #         raise CustomValidationError(detail=_("Ism va familiya kiritilishi shart"))
    #     birth_date = attrs.get('birth_date', None)
    #     if birth_date is None:
    #         raise CustomValidationError(detail=_("Tugilgan sana kiritilishi shart"))
    #     gender = attrs.get('gender', None)
    #     if gender is None:
    #         raise CustomValidationError(detail=_("Jins kiritilishi shart"))
    #     passport = attrs.get('passport', None)
    #     if passport is None:
    #         raise CustomValidationError(detail=_("Passport seriya kiritilishi shart"))
    #     passport_image = attrs.get('passport_image', None)
    #     if passport_image is None:
    #         raise CustomValidationError(detail=_("Passport rasmi kiritilishi shart"))
    #     passport_image2 = attrs.get('passport_image2', None)
    #     if passport_image2 is None:
    #         raise CustomValidationError(
    #             detail=_("Passport ushlab tushilgan rasm biriktilishi shart shart.(yuz ko'ringan xolatda)"))
    #     diplom_image = attrs.get('diplom_image', None)
    #     if diplom_image is None:
    #         raise CustomValidationError(
    #             detail=_("Diplom yoki sertifikat rasmi kiritilishi shart"))
    #     bio = attrs.get('bio', None)
    #     if bio is None:
    #         raise CustomValidationError(
    #             detail=_("Mutaxassislik haqida malumotnoma kiritlishi kerak"))

class SuccessDoctorApplicationSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)

    class Meta:
        model = DoctorApplication
        fields = ['id', 'user', 'image', 'region', 'district', 'address', 'full_name', 'birth_date', 'gender', 'passport',
                  'experience_year', 'passport_image', 'passport_image2', 'diplom_image', 'bio', 'status', 'created_at', 'term']