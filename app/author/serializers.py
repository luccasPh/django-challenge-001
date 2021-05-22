from rest_framework import serializers

from .models import Author


class AuthorSerializer(serializers.ModelSerializer):
    picture = serializers.SerializerMethodField(source="picture", method_name="get_picture")
    class Meta:
        model = Author
        fields = ["id", "name", "picture"]
        read_only_fields = ["id", "picture"]

    def get_picture(self, obj):
        if not obj.picture:
            return None

        return self.context["request"].build_absolute_uri(obj.picture.url)


class PictureAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["picture"]
