from rest_framework import serializers
from users.serializer import UserUsernameSerializer
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    created_by = UserUsernameSerializer(read_only=True)
    modified_by = UserUsernameSerializer(read_only=True)

    # File size is not validated here, because it implies having to completely upload the size before querying it
    # This should be handled in the server settings. It could be added here as an extra safe-keep to avoid keeping
    # a very large file occupying space on disk.

    class Meta:
        model = Customer
        fields = ("id", "name", "surname", "photo", "created_by", "modified_by")
