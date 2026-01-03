from rest_framework.generics import RetrieveAPIView

from apps.profile.permission import DoctorProfilePermission, PatientProfilePermission
from apps.profile.serializers.profiles import GET_ROLE_SERIALIZER
from apps.utils.CustomResponse import CustomResponse
from apps.utils.role_validate import RoleValidate


class UserProfileRetrieveAPIView(RetrieveAPIView):
    """
    User profil qismi malumotlarni olish
    """
    permission_classes = [DoctorProfilePermission, PatientProfilePermission]

    def get_object(self):
        role_model = RoleValidate.get_role_model(self.request)
        return role_model.objects.get(
            user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        role = RoleValidate.get_role(request)
        serializer = GET_ROLE_SERIALIZER.get(role)
        obj = self.get_object()
        serializer = serializer(obj)
        return CustomResponse.success_response(
            data=serializer.data
        )
