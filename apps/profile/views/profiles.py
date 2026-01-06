from drf_spectacular.utils import extend_schema
from rest_framework.generics import RetrieveAPIView

from apps.profile.permission import  UserProfilePermission
from apps.profile.serializers.profiles import GET_ROLE_SERIALIZER
from apps.utils.CustomResponse import CustomResponse
from apps.utils.role_validate import RoleValidate

@extend_schema(summary='🔐 login qilgan hamma uchun')
class UserProfileRetrieveAPIView(RetrieveAPIView):
    """
    User profil qismi malumotlarni olish
    """
    permission_classes = [UserProfilePermission]

    def get_object(self):
        role_model = RoleValidate.get_role_model(self.request)
        return role_model.objects.get(
            user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        role = RoleValidate.get_role(request)
        print(role)
        print(RoleValidate.get_token_active_role(request))
        print(RoleValidate.get_profile_user(request))
        serializer = GET_ROLE_SERIALIZER.get(role)
        print(serializer)
        obj = self.get_object()
        print(obj)
        serializer = serializer(obj)
        return CustomResponse.success_response(
            data=serializer.data
        )
