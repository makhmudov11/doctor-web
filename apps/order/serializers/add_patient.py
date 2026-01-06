from datetime import date

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from apps.order.models import AddPatient
from apps.profile.serializers.profiles import PatientProfileSerializer
from apps.utils.CustomValidationError import CustomValidationError
from apps.utils.base_models import GenderChoices


class AddPatientCreateSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateField(
        input_formats=["%d.%m.%Y", "%d/%m/%Y"],
        required=True
    )
    gender = serializers.ChoiceField(choices=GenderChoices.choices, required=True)

    class Meta:
        model = AddPatient
        fields = ['image', 'full_name', 'birth_date', 'gender']
        extra_kwargs = {
            "full_name" : {"required" : True}
        }

    def validate(self, attrs):
        full_name = attrs.get('full_name', None)
        birth_date = attrs.get('birth_date', None)
        if full_name is None:
            raise CustomValidationError(
                detail=_("Ism va familiya kiritilishi shart")
            )
        if birth_date > date.today():
            raise CustomValidationError(detail=_("Tug'ilgan sana kelajakda bo'lishi mumkin emas"))

        return attrs

class AddPatientDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddPatient
        fields = ['id', 'full_name', 'image', 'birth_date', 'gender', 'is_self', 'created_at']

class UserAddPatientListSerializer(serializers.Serializer):
    patient = PatientProfileSerializer(read_only=True)
    add_patients = serializers.SerializerMethodField()

    def get_add_patients(self, obj):
        qs = obj.get('add_patients')
        if not qs.exists():
            return [AddPatientDetailSerializer().data]
        return AddPatientDetailSerializer(instance=qs, many=True).data