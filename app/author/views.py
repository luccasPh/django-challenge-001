from uuid import UUID
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from drf_yasg.utils import swagger_auto_schema

from .models import Author
from .serializers import AuthorSerializer, PictureAuthorSerializer

from .docs import schemas


class CreateAuthorView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(**schemas.create)
    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class PictureAuthorView(APIView):
    parser_classes = [MultiPartParser]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            UUID(pk)
        except Exception:
            raise ValidationError({"id": ["Author id invalid"]})

        queryset = Author.objects.filter(id=pk).first()
        if not queryset:
            raise NotFound({"detail": "Author not found"})

        return queryset

    @swagger_auto_schema(**schemas.picture)
    def patch(self, request, pk):
        queryset = self.get_object(pk)
        serializer = PictureAuthorSerializer(
            instance=queryset,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        serializer = AuthorSerializer(instance=instance, context={"request": request})
        return Response(data=serializer.data)


class AuthorView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            UUID(pk)
        except Exception:
            raise ValidationError({"id": ["Author id invalid"]})

        queryset = Author.objects.filter(id=pk).first()
        if not queryset:
            raise NotFound({"detail": "Author not found"})

        return queryset

    @swagger_auto_schema(**schemas.retrive)
    def get(self, request, pk):
        queryset = self.get_object(pk)
        serialize = AuthorSerializer(instance=queryset, context={"request": request})
        return Response(data=serialize.data)

    @swagger_auto_schema(**schemas.update)
    def put(self, request, pk):
        queryset = self.get_object(pk)
        serialize = AuthorSerializer(
            instance=queryset, data=request.data, context={"request": request}
        )
        serialize.is_valid(raise_exception=True)
        serialize.save()

        return Response(data=serialize.data)

    @swagger_auto_schema(**schemas.delete)
    def delete(self, request, pk):
        queryset = self.get_object(pk)
        queryset.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
