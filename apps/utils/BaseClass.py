from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK

from apps.users.models import SmsCodeTypeChoices
from apps.users.serializers.user_detail import UserFullDataSerializer
from apps.utils.CustomResponse import CustomResponse
from django.utils.translation import gettext_lazy as _


class BaseVerifyCode:

    @classmethod
    def sms_code_type_response(cls, user_code_obj, user):
        if user_code_obj._type == SmsCodeTypeChoices.REGISTER:
            user.status = True
            user.save()
            user_code_obj.verified = True
            user_code_obj.save(update_fields=['verified'])
            return CustomResponse.success_response(
                message=_("Registratsiya muvaffaqiyatli bajarildi, foydalanuvchi yaratildi"),
                data=UserFullDataSerializer(user).data, code=HTTP_201_CREATED)
        elif user_code_obj._type == SmsCodeTypeChoices.CHANGE_PASSWORD:
            user_code_obj.verified = True
            user_code_obj.save(update_fields=['verified'])
            return CustomResponse.success_response(
                message=_("Parol o'zgartirish uchun kod tasdiqlandi"),
                data={"user": UserFullDataSerializer(user).data}, code=HTTP_200_OK
            )
        elif user_code_obj._type == SmsCodeTypeChoices.UPDATE_CONTACT:
            user_code_obj.verified = True
            user_code_obj.save(update_fields=['verified'])
            return CustomResponse.success_response(
                message=_('Kod tasdiqlandi'), code=HTTP_200_OK
            )
        else:
            return CustomResponse.error_response(
                message=_("Xabar turi aniqlanmadi")
            )
