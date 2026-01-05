from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from django.utils.translation import gettext_lazy as _
from rest_framework.parsers import MultiPartParser, FormParser

from apps.order.models import AddPatient
from apps.order.serializers.add_patient import AddPatientSerializer, UserAddPatientListSerializer
from apps.profile.permission import IsPatient
from apps.utils.CustomResponse import CustomResponse
from apps.utils.role_validate import RoleValidate


class AddPatientCreateAPIView(CreateAPIView):
    serializer_class = AddPatientSerializer
    permission_classes = [IsPatient]
    parser_classes = [MultiPartParser, FormParser]
    queryset = AddPatient.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = RoleValidate.get_profile_user(request)
        serializer.save(patient=profile)
        return CustomResponse.success_response(
            message=_("Bemor muvaffaqiyatli qo'shildi"),
            data=serializer.data,
            code=status.HTTP_201_CREATED
        )

class UserAddPatientListAPIView(ListAPIView):
    serializer_class = UserAddPatientListSerializer
    permission_classes = [IsPatient]

    def get_queryset(self):
        return AddPatient.objects.filter(patient=RoleValidate.get_profile_user(self.request))

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        profile = RoleValidate.get_profile_user(request)

        serializer = self.get_serializer({
            "patient" : profile,
            "patients" : queryset
        })
        return CustomResponse.success_response(data=serializer.data)

