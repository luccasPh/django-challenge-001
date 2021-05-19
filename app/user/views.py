from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import SignUpSerializer, LoginSerializer


class SignUpUserView(generics.CreateAPIView):
    serializer_class = SignUpSerializer


class LoginUserView(ObtainAuthToken):
    serializer_class = LoginSerializer
