from django.conf import settings
import base64
from decimal import Decimal

from apps.utils.CustomValidationError import CustomValidationError


class PayComResponse(object):
    LINK = 'https://checkout.paycom.uz'

    def __init__(self):
        self.TOKEN = None
        self.KEY = None

    def check_kassa(self):
        try:
            self.TOKEN = settings.PAYCOM_SETTINGS['KASSA_ID']
            self.KEY = settings.PAYCOM_SETTINGS['ACCOUNTS']['KEY']
            if not self.TOKEN or not self.KEY:
                raise CustomValidationError("Kassa malumotlari topilmadi")
        except Exception as e:
            raise CustomValidationError(detail="Kassa malumotlarini olishda xatolik")

    def create_initialization(self, amount: int, balance_id: str, return_url: str) -> str:

        self.check_kassa()
        params = f"m={self.TOKEN};ac.{self.KEY}={balance_id};a={amount};c={return_url}"
        encode_params = base64.b64encode(params.encode("utf-8"))
        encode_params = str(encode_params, 'utf-8')
        url = f"{self.LINK}/{encode_params}"
        return url
