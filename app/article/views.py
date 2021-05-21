from uuid import UUID
from django.http.request import HttpRequest
from rest_framework import status
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Article
from .serializers import (
    ArticleSerializer,
    AnonymousArticleSerializer,
    ListArticleSerializer,
)


class AdminArticleView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def validate(self, pk):
        try:
            UUID(pk)
            return True
        except Exception:
            return False

    def get_queryset(self, pk):
        if not pk:
            return Article.objects.all().first()

        if not self.validate(pk):
            raise ValidationError({"id": ["Article id invalid"]})

        if not Article.objects.filter(id=pk).exists():
            raise NotFound({"message": ["Article not found"]})

        return Article.objects.filter(id=pk).first()

    def post(self, request: HttpRequest):
        serializer = ArticleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request: HttpRequest, pk=None):
        queryset = self.get_queryset(pk)
        serializer = ArticleSerializer(instance=queryset, context={"request": request})

        return Response(data=serializer.data)

    def put(self, request: HttpRequest, pk=None):
        queryset = self.get_queryset(pk)
        serializer = ArticleSerializer(
            instance=queryset, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: HttpRequest, pk=None):
        queryset = self.get_queryset(pk)
        queryset.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ListArticleView(APIView):
    def get(self, request: HttpRequest):
        category = request.query_params.get("category", None)
        if not category:
            raise ValidationError(
                {"message": ["Missing required argument: 'category'"]}
            )

        queryset = Article.objects.filter(category=category).all()
        serializer = ListArticleSerializer(
            instance=queryset, many=True, context={"request": request}
        )
        return Response(data=serializer.data)


class DetailArticleView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def get_queryset(self, pk):
        try:
            UUID(pk)
        except Exception:
            raise ValidationError({"id": ["Article id invalid"]})

        queryset = Article.objects.filter(id=pk).first()
        if not queryset:
            raise NotFound({"message": ["Article not found"]})

        return queryset

    def get(self, request: HttpRequest, pk=None):
        queryset = self.get_queryset(pk)
        if request.user.is_authenticated:
            serializer = ArticleSerializer(instance=queryset)

        else:
            serializer = AnonymousArticleSerializer(instance=queryset)

        return Response(serializer.data)
