from rest_framework import serializers
from users.serializer import UserUsernameSerializer
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    created_by = UserUsernameSerializer(read_only=True)
    modified_by = UserUsernameSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = ("id", "name", "surname", "photo", "created_by", "modified_by")
