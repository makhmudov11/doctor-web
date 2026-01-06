from traceback import print_tb

from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from apps.history.models import Address
from apps.history.serializers.address import AddressSerializer, AddressCreateSerializer, AddressFullDataSerializer
from apps.profile.models import PatientProfile
from apps.profile.permission import IsPatient
from apps.utils.CustomResponse import CustomResponse
from apps.utils.role_validate import RoleValidate
from django.utils.translation import gettext_lazy as _


@extend_schema(summary='🔐 patient uchun adresslar listi')
class PatientAddressAPIView(APIView):
    permission_classes = [IsPatient]

    def get(self, request, patient_public_id):
        if not patient_public_id:
            return CustomResponse.error_response(
                message=_("Bemor id kelishi shart")
            )
        try:
            profile = PatientProfile.objects.get(public_id=patient_public_id, status=True)
        except PatientProfile.DoesNotExist:
            return CustomResponse.error_response(
                message=_("Bemor profili topilmadi"),
                code=HTTP_404_NOT_FOUND
            )
        if profile.public_id != patient_public_id:
            return CustomResponse.error_response(
                message=_("Siz faqat o'zingizning manzillaringizni ko'ra olasiz")
            )

        data = Address.objects.filter(patient=profile, status=True)
        if not data.exists():
            return CustomResponse.error_response(
                message=_("Bemorga tegishli adresslar topilmadi")

            )
        serializer = AddressSerializer(instance=data, many=True)
        return CustomResponse.success_response(
            data=serializer.data
        )


@extend_schema(summary='🔐 patient uchun adress create')
class AddressCreateAPIView(CreateAPIView):
    serializer_class = AddressCreateSerializer
    # permission_classes = [IsPatient]
    queryset = Address.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = RoleValidate.get_profile_user(request)
        data = serializer.save(patient=profile)
        serializer = AddressFullDataSerializer(instance=data)
        return CustomResponse.success_response(
            data=serializer.data
        )


@extend_schema(summary='🔐 patient uchun adress delete')
class AddressDeleteAPIView(APIView):
    permission_classes = [IsPatient]

    def delete(self, request, address_id):
        if not address_id:
            return CustomResponse.error_response(
                message=_("Address id kelishi shart")
            )
        profile = RoleValidate.get_profile_user(request)
        try:
            address_obj = Address.objects.get(id=address_id, status=True, patient=profile)
        except Address.DoesNotExist:
            return CustomResponse.error_response(
                message=_("Address topilmadi")
            )
        address_obj.status = False
        address_obj.save(update_fields=['status'])
        return CustomResponse.error_response(
            message=_("Address muvaffaqiyatli o'chirildi")
        )


@extend_schema(summary='🔐 patient uchun adress detaili')
class AddressDetailAPIView(APIView):
    permission_classes = [IsPatient]

    def get(self, request, address_id):
        if not address_id:
            return CustomResponse.error_response(
                message=_("Address id kelishi shart")
            )
        profile = RoleValidate.get_profile_user(request)
        try:
            print(profile)
            address_obj = Address.objects.get(id=address_id, status=True, patient=profile)
            print(address_obj)
        except Address.DoesNotExist:
            return CustomResponse.error_response(
                message=_("Address topilmadi")
            )
        serializer = AddressFullDataSerializer(instance=address_obj)
        return CustomResponse.error_response(
            data=serializer.data
        )
