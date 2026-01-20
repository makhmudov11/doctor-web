from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.history.serializers.address import AddressFullDataSerializer
from apps.order.models import Order, PaymentTypeChoice, OrderDetailImage, OrderDetail, MedicalService
from apps.order.serializers.add_patient import AddPatientDetailSerializer
from apps.profile.models import DoctorProfile
from apps.profile.serializers.profiles import PatientProfileSerializer, DoctorProfileSerializer
from apps.transactions.serializers import UserTransactionHistorySerializer
from apps.utils.CustomValidationError import CustomValidationError

from django.utils.translation import gettext_lazy as _


class MedicalServiceSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    count = serializers.IntegerField(min_value=1)


class OrderCreateSerializer(serializers.ModelSerializer):
    add_patient = serializers.IntegerField()
    address_id = serializers.IntegerField()
    services = serializers.JSONField(required=False)  # MedicalServiceSerializer(many=True, required=False)
    prescription = serializers.ListField(
        child=serializers.FileField(),
        required=False,
        default=list
    )

    payment_type = serializers.ChoiceField(choices=PaymentTypeChoice.choices, required=True)
    summa = serializers.IntegerField()
    doctor = serializers.SlugRelatedField(
        slug_field='public_id',
        queryset=DoctorProfile.objects.all(),
        required=True
    )

    class Meta:
        model = Order
        fields = ['add_patient', 'address_id',
                  'prescription', 'doctor', 'services', 'payment_type', 'summa']
        extra_kwargs = {
            "prescription": {"required": False},
            "services": {"required": False},
        }

    def validate_services(self, value):
        if not value:
            return []

        serializer = MedicalServiceSerializer(data=value, many=True)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    def validate(self, attrs):
        add_patient = attrs.get('add_patient', None)
        if add_patient is None:
            raise CustomValidationError(detail=_("Bemor id kelishi shart"))

        address_id = attrs.get('address_id', None)
        if address_id is None:
            raise CustomValidationError(detail=_("Manzil id kelishi shart"))
        payment_type = attrs.get('payment_type', None)
        if payment_type is None:
            raise CustomValidationError(detail=_("To'lov turi aniqlanmadi"))
        summa = attrs.get('summa', None)
        if summa is None or not isinstance(summa, int):
            raise CustomValidationError(
                detail=_(f"Summa bilan muammo {"(summa aniqlanmadi)" if summa is None else "summa int bolishi kerak"}"
                         )
            )
        return attrs


class OrderImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetailImage
        fields = ['prescription']


class OrderDetailFullSerializer(serializers.ModelSerializer):
    patient = PatientProfileSerializer(read_only=True)
    add_patient = AddPatientDetailSerializer(read_only=True)
    doctor = DoctorProfileSerializer(read_only=True)
    address = AddressFullDataSerializer(read_only=True)
    detail = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'order_id', 'patient', 'doctor', 'add_patient', 'address',
            'payment_type', 'status', 'summa', 'detail'
        ]

    def get_detail(self, obj):
        images = obj.order_images.all()
        order_details = obj.order_details.all()

        service_ids = set()
        for od in order_details:
            for s in od.medical_service:
                service_ids.add(s['id'])

        services_map = {
            s.id: s for s in MedicalService.objects.filter(id__in=service_ids)
        }

        services_list = []
        for od in order_details:
            for s in od.medical_service:
                service_obj = services_map.get(s['id'])
                if not service_obj:
                    continue
                services_list.append({
                    "id": service_obj.id,
                    "name": service_obj.name,
                    "description": service_obj.description,
                    "price": service_obj.price,
                    "count": s.get('count', 1)
                })

        return {
            "images": OrderImageSerializer(images, many=True, context=self.context).data,
            "services": services_list
        }

class OrderHistoryAndBalanceSerializer(serializers.ModelSerializer):
    data_type = serializers.CharField(default='order', read_only=True)

    class Meta:
        model = Order
        fields = ['data_type', 'created_at', 'order_id', 'summa', 'status']

class UserHistoryResponseSerializer(serializers.Serializer):
    orders = OrderHistoryAndBalanceSerializer()
    transactions = UserTransactionHistorySerializer()
