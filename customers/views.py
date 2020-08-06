from rest_framework import permissions, viewsets

from .serializer import CustomerSerializer
from .models import Customer

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, OAuth2Authentication

class CustomersViewSet(viewsets.ModelViewSet):
    """
        retrieve:
        Return the given customer, filter by id.

        list:
        Return a list of all the existing customers.

        create:
        Create a new customer.

        update:
        Updates given customer, all required information must be passed in update.

        partial_update:
        Update any information of the given customer.

        destroy:
        Delete the given customer
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    authentication_classes = [OAuth2Authentication]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, modified_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)
