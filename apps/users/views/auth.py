from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from apps.notifications.models import FCMDevice
from apps.users.models import SmsCodeTypeChoices, UserContactTypeChoices, SmsCode
from apps.users.serializers.auth import RegisterSerializer, LoginSerializer
from apps.users.serializers.user_detail import UserFullDataSerializer

from apps.users.tasks import send_verification_code
from apps.utils.CustomResponse import CustomResponse
from apps.utils.eskiz import EskizUZ
from apps.utils.generate_code import generate_code
from apps.utils.token_claim import get_tokens_for_user, token_blacklist
from drf_spectacular.utils import extend_schema

User = get_user_model()


@extend_schema(summary='🔐 hamma uchun')
class RegisterCreateAPIView(CreateAPIView):
    """
    Ro'yhatdan o'tish
    """
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        contact = request.data.get('contact', '').strip()
        if not contact:
            return CustomResponse.error_response(
                message=_("Email yoki telefon raqam kiritilishi shart"),
                code=status.HTTP_400_BAD_REQUEST
            )
        if User.objects.filter(contact=contact, status=True).exists():
            return CustomResponse.error_response(
                message=_(f"{contact} orqali avval ro'yhatdan o'tilgan"),
            )
        User.objects.filter(contact=contact, status=False).delete()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        contact_type = serializer.validated_data.get('contact_type')

        code = generate_code()
        try:
            SmsCode.create_for_contact(
                contact=contact,
                code=code,
                _type=SmsCodeTypeChoices.REGISTER
            )
        except Exception as e:
            return CustomResponse.error_response(message='Kod saqlashda xatolik.',
                                                 code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        user = serializer.save()
        user = UserFullDataSerializer(user).data

        if contact_type == UserContactTypeChoices.EMAIL:
            try:
                send_verification_code(email=contact, code=code)
            except Exception as e:
                return CustomResponse.error_response(
                    message=_('Kod yuborishda xatolik'),
                )

        else:
            phone = contact.lstrip('+')
            send_code = EskizUZ.send_sms_phone_number(phone_number=phone, code=code)
            if not send_code['success']:
                return CustomResponse.error_response(
                    message=send_code['message'],
                    data=send_code['data']
                )
        return CustomResponse.success_response(
            message='Kod muvaffaqiyatli yuborildi',
            data=user
        )

@extend_schema(summary='🔐 hamma uchun')
class LoginAPIView(APIView):
    """
    Login qilish
    """
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        contact = serializer.validated_data.get('contact').strip()
        password = serializer.validated_data.get('password').strip()

        try:
            user = User.objects.get(contact=contact, status=True, is_active=True)
        except User.DoesNotExist:
            return CustomResponse.error_response(message=_("User topilmadi"), code=HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return CustomResponse.error_response(message=_("Parol noto'g'ri"), code=HTTP_401_UNAUTHORIZED)

        fcm_token = serializer.validated_data.get('fcm_token', None)

        try:
            with transaction.atomic():
                if fcm_token:
                    device_obj = FCMDevice(
                        user=user,
                        token=fcm_token)
                    device_type=serializer.validated_data.get('device_type', None)
                    if device_type:
                        device_obj.device_type = device_type
                    device_obj.save()
        except Exception as e:
            return CustomResponse.error_response(
                message=_(f"Xatolik: {str(e)}")
            )
        token = get_tokens_for_user(user)
        return CustomResponse.success_response(
            message=_("Login muvaqqiyatli yakunlandi"),
            data={"user": UserFullDataSerializer(user).data, "token": token}, code=status.HTTP_200_OK
        )

@extend_schema(summary='🔐 login qilgan hamma uchun')
class UserLogoutAPIView(APIView):
    """
    Akkauntdan chiqish
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            token_blacklist(request)
        except Exception as e:
            return CustomResponse.error_response(
                message=_(f"Xatolik yuz berdi {str(e)}"),
                code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        CustomResponse.success_response(
            message=_("Chiqish muvaffaqiyatli bajarildi. Shu foydalanuvchining barcha tokenlari endi ishlamaydi.")
        )

@extend_schema(summary='🔐 login qilgan hamma uchun')
class UserDeleteAccount(APIView):
    """
    Akkauntni butunlay o'chirish
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            token_blacklist(request)
        except Exception as e:
            return CustomResponse.error_response(
                message=_(f"Xatolik yuz berdi, {str(e)}"),
                code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        request.user.is_active = False
        return CustomResponse.success_response(
            message=_("Muvaffaqiyatli o'chirildi"),
            code=status.HTTP_204_NO_CONTENT
        )
