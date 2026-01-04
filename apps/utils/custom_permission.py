from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from django.utils.translation import gettext_lazy as _

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, PermissionDenied):
        return Response({
            "success": False,
            "message": _("Sizga bu obyektga kirish huquqi yo‘q"),
            "code": 403
        }, status=status.HTTP_403_FORBIDDEN)

    if isinstance(exc, NotAuthenticated):
        return Response({
            "success": False,
            "message": _("Foydalanuvchi autentifikatsiyadan o‘tmagan"),
            "code": 401
        }, status=status.HTTP_401_UNAUTHORIZED)

    return response
