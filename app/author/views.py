from uuid import UUID
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
)

from .models import Author
from .serializers import AuthorSerializer, AuthorUploadSerializer


class CreateAuthorView(CreateAPIView):
    serializer_class = AuthorSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]


class DetailAuthorView(RetrieveUpdateDestroyAPIView):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def validate(self, author_id):
        try:
            UUID(author_id)
            return True
        except Exception:
            return False

    def get_queryset(self):
        author_id = self.kwargs["pk"]
        if not self.validate(author_id):
            raise ValidationError({"id": ["Author id invalid"]})

        if not self.queryset.filter(id=author_id).exists():
            raise NotFound({"message": ["Author not found"]})

        return self.queryset.filter(id=author_id)


class UploadAuthorView(UpdateAPIView):
    serializer_class = AuthorUploadSerializer
    queryset = Author.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def validate(self, author_id):
        try:
            UUID(author_id)
            return True
        except Exception:
            return False

    def get_queryset(self):
        author_id = self.kwargs["pk"]
        if not self.validate(author_id):
            raise ValidationError({"id": ["Author id invalid"]})

        if not self.queryset.filter(id=author_id).exists():
            raise NotFound({"message": ["Author not found"]})

        return self.queryset.filter(id=author_id)
