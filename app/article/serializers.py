from django.apps import apps
from rest_framework import serializers

from .models import Article


class AuthorSerializer(serializers.ModelSerializer):
    picture = serializers.SerializerMethodField(source="picture")

    class Meta:
        ref_name = None
        model = apps.get_model("author", "Author")
        fields = ["id", "name", "picture"]

    def get_picture(self, obj):
        if not obj.picture:
            return None

        return self.context["request"].build_absolute_uri(obj.picture.url)


class ArticleSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(source="author_id", read_only=True)

    class Meta:
        model = Article
        fields = "__all__"
        read_only_fields = ["id", "author"]
        extra_kwargs = {"author_id": {"write_only": True}}


class ListArticleSerializer(ArticleSerializer):
    class Meta(ArticleSerializer.Meta):
        fields = ["id", "author", "category", "title", "summary"]


class AnonymousArticleSerializer(ArticleSerializer):
    class Meta(ArticleSerializer.Meta):
        fields = ["id", "author", "category", "title", "summary", "firstParagraph"]
