from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "password", "email", "is_superuser")

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data.get("password"))
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        user.set_password(validated_data.get("password"))
        user.save()
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["is_admin"] = data["is_superuser"]
        data.pop("is_superuser")
        return data

    def to_internal_value(self, data):
        if "is_admin" in data:
            new_data = data.copy()
            new_data["is_superuser"] = data["is_admin"]
            new_data.pop("is_admin")
            return super().to_internal_value(new_data)
        return super().to_internal_value(data)


class UserUsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "username")


class TokenSerializer(serializers.Serializer):
    """
    Serialize token
    """
    token = serializers.CharField(max_length=255)