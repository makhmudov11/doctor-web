from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed, TokenError

from apps.utils.CustomResponse import CustomResponse
from apps.utils.CustomValidationError import CustomValidationError


def get_tokens_for_user(user):
    if not user.is_active:
        raise AuthenticationFailed("User is not active")

    update_last_login(sender=None, user=user)
    refresh = RefreshToken.for_user(user)
    refresh['active_role'] = user.active_role

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def get_token_jwt(request):
    auth_header = request.headers.get('Authorization')
    if auth_header is None:
        token = None
    else:
        token = auth_header.split(' ')[1] if ' ' in auth_header else None
    if token is None:
        raise CustomValidationError(
            detail="Token topilmadi"
        )
    return token


def token_blacklist(request):
    user = request.user
    tokens = OutstandingToken.objects.filter(user=user)
    for token_obj in tokens:
        BlacklistedToken.objects.get_or_create(token=token_obj)

    # 2️⃣ Requestdagi access tokenni alohida blacklist qilish (agar OutstandingToken da bo'lsa)
    auth_header = request.headers.get("Authorization")
    if auth_header:
        try:
            token_str = auth_header.split()[1]  # Bearer <token>
            access_token = AccessToken(token_str)
            token_obj = OutstandingToken.objects.filter(jti=access_token['jti']).first()
            if token_obj:
                BlacklistedToken.objects.get_or_create(token=token_obj)
        except (IndexError, TokenError):
            pass  # Token expired bo‘lsa ham xatolik bermaydi

    return True