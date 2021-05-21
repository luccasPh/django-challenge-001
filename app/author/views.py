from uuid import UUID
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Author
from .serializers import AuthorSerializer, AuthorUploadSerializer


class AuthorView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get_queryset(self, pk):
        try:
            UUID(pk)
        except Exception:
            raise ValidationError({"id": ["Author id invalid"]})

        queryset = Author.objects.filter(id=pk).first()
        if not queryset:
            raise NotFound({"message": ["Author not found"]})

        return queryset

    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, pk=None):
        queryset = self.get_queryset(pk)
        serialize = AuthorSerializer(instance=queryset, context={"request": request})
        return Response(data=serialize.data)

    def put(self, request, pk=None):
        queryset = self.get_queryset(pk)
        serialize = AuthorSerializer(
            instance=queryset, data=request.data, context={"request": request}
        )
        serialize.is_valid(raise_exception=True)
        serialize.save()

        return Response(data=serialize.data)

    def patch(self, request, pk=None):
        queryset = self.get_queryset(pk)
        serializer = AuthorUploadSerializer(
            instance=queryset,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data)

    def delete(self, request, pk=None):
        queryset = self.get_queryset(pk)
        queryset.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
