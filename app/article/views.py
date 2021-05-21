from uuid import UUID
from django.http.request import HttpRequest
from rest_framework import status
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from .docs import schemas
from .models import Article
from .serializers import (
    ArticleSerializer,
    AnonymousArticleSerializer,
    ListArticleSerializer,
)


class AdminCreateArticleView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(**schemas.admin_create)
    def post(self, request: HttpRequest):
        serializer = ArticleSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class AdminArticleView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get_objet(self, pk):
        try:
            UUID(pk)
        except Exception:
            raise ValidationError({"id": ["Article id invalid"]})

        queryset = Article.objects.filter(id=pk).first()
        if not queryset:
            raise NotFound({"message": ["Article not found"]})

        return queryset

    @swagger_auto_schema(**schemas.admin_retrive)
    def get(self, request: HttpRequest, pk):
        queryset = self.get_objet(pk)
        serializer = ArticleSerializer(instance=queryset, context={"request": request})

        return Response(data=serializer.data)

    @swagger_auto_schema(**schemas.admin_update)
    def put(self, request: HttpRequest, pk):
        queryset = self.get_objet(pk)
        serializer = ArticleSerializer(
            instance=queryset, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(**schemas.admin_delete)
    def delete(self, request: HttpRequest, pk):
        queryset = self.get_objet(pk)
        queryset.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ListArticleView(APIView):
    @swagger_auto_schema(**schemas.list)
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

    def get_objet(self, pk):
        try:
            UUID(pk)
        except Exception:
            raise ValidationError({"id": ["Article id invalid"]})

        queryset = Article.objects.filter(id=pk).first()
        if not queryset:
            raise NotFound({"message": ["Article not found"]})

        return queryset

    @swagger_auto_schema(**schemas.detail)
    def get(self, request: HttpRequest, pk):
        queryset = self.get_objet(pk)
        if request.user.is_authenticated:
            serializer = ArticleSerializer(
                instance=queryset, context={"request": request}
            )

        else:
            serializer = AnonymousArticleSerializer(
                instance=queryset, context={"request": request}
            )

        return Response(serializer.data)
