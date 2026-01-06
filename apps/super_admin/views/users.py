from django.contrib.auth import get_user_model, authenticate
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import filters, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from apps.super_admin.filters.users import UserListFilter
from apps.super_admin.paginations.users import AdminUserListPagination
from apps.super_admin.permissions.users import AdminPermission
from apps.super_admin.serializers.users import AdminUserListSerializer, AdminUserCreateSerializer, \
    AdminUserRetrieveUpdateDestroySerializer, AdminLoginSerializer
from apps.utils.CustomResponse import CustomResponse
from apps.utils.token_claim import get_tokens_for_user

User = get_user_model()


class AdminUserListAPIView(ListAPIView):
    permission_classes = [AdminPermission]
    serializer_class = AdminUserListSerializer
    pagination_class = AdminUserListPagination
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'is_staff']
    filterset_class = UserListFilter
    search_fields = ['full_name', 'contact', 'role', 'contact_type', 'gender']
    ordering_fields = ['created_at', 'full_name']
    ordering = ['-created_at']


class AdminUserCreateAPIView(CreateAPIView):
    serializer_class = AdminUserCreateSerializer
    permission_classes = [AdminPermission]
    queryset = User.objects.all()

    parser_classes = [MultiPartParser, FormParser]


class AdminUserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = AdminUserRetrieveUpdateDestroySerializer
    permission_classes = [AdminPermission]
    queryset = User.objects.all()
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.deleted_at = timezone.now()
        instance.save(update_fields=['is_active', 'deleted_at'])

        return CustomResponse.success_response(
            message="Foydalanuvchi muvaffaqiyatli o'chirildi",
            code=status.HTTP_204_NO_CONTENT
        )

class AdminLoginAPIView(APIView):
    """
    Faqat is_staff=True bo'lgan userlar uchun admin login.
    """
    serializer_class = AdminLoginSerializer
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return CustomResponse.error_response(message=_("Username va password kiritilishi shart"),
                                                 code=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:
                token = get_tokens_for_user(user)
                return CustomResponse.success_response(data=token)
            else:
                return CustomResponse.error_response(message=_("Siz admin emassiz"), code=status.HTTP_403_FORBIDDEN)
        return CustomResponse.error_response(message=_("Username yoki parol noto‘g‘ri"),
                                             code=status.HTTP_401_UNAUTHORIZED)
