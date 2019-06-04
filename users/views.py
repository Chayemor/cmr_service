from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework_jwt.settings import api_settings

from .serializer import UserSerializer, TokenSerializer
from .permissions import IsSuperUser

# JWT settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UsersViewSet(viewsets.ModelViewSet):
    """
        retrieve:
        Return the given user, filter by id.

        list:
        Return a list of all the existing users.

        create:
        Create a new user.

        update:
        Updates given user, all required information must be passed in update.

        partial_update:
        Update any information of the given user.

        destroy:
        Delete the given user
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsSuperUser,)