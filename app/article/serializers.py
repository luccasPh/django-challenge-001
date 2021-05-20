from django.apps import apps
from rest_framework import serializers

from .models import Article


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model("author", "Author")
        fields = "__all__"

    def get_picture(self, obj):
        if not obj.picture:
            return obj

        return self.context["request"].build_absolute_uri(obj.picture.url)


class ArticleSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(source="author_id", read_only=True)

    class Meta:
        model = Article
        fields = "__all__"
        read_only_fields = ["id"]
        extra_kwargs = {"author_id": {"write_only": True}}
