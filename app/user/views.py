from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from .serializers import SignUpSerializer, LoginSerializer
from .docs import schemas


class SignUpUserView(APIView):
    @swagger_auto_schema(**schemas.signup)
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class LoginUserView(ObtainAuthToken):
    serializer_class = LoginSerializer

    @swagger_auto_schema(**schemas.login)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
