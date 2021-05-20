from rest_framework import serializers

from .models import Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "picture"]
        read_only_fields = ["id", "picture"]

    def create(self, validated_data):
        return Author.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name")
        instance.save()

        return instance


class AuthorUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["picture"]
