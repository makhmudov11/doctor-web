from rest_framework.response import Response
from rest_framework import status


class CustomResponse:
    @staticmethod
    def success_response(data=None, message="Success", code=status.HTTP_200_OK):
        if data is None:
            data = []
        return Response({
            "success": True,
            "message": message,
            "data": data
        }, status=code)

    @staticmethod
    def error_response(data=None, message="Error", code=status.HTTP_400_BAD_REQUEST):
        if data is None:
            data = []
        return Response({
            "success": False,
            "message": message,
            "data": data
        }, status=code)
