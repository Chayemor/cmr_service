from rest_framework import status, viewsets

from .serializer import CustomerSerializer
from .models import Customer


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

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, modified_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)