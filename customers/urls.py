from .routers import OptionalSlashRouter
from .views import CustomersViewSet


router = OptionalSlashRouter()
router.register('customers', CustomersViewSet, basename="customers")

urlpatterns = []

urlpatterns += router.urls
