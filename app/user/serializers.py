from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class SignUpSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ["email", "password", "password_confirmation"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        validated_data.pop("password_confirmation")
        return get_user_model().objects.create_user(**validated_data)

    def validate(self, data):
        password = data["password"]
        password_confirmation = data["password_confirmation"]
        if password != password_confirmation:
            raise ValidationError({"password": ["Passwords dont match"]})
        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs["email"]
        password = attrs["password"]

        user = authenticate(
            request=self.context.get("request"), username=email, password=password
        )
        if not user:
            raise ValidationError({"message": ["Invalid email or password"]})

        attrs["user"] = user
        return attrs
