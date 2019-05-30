from .routers import OptionalSlashRouter
from .views import CustomersViewSet


router = OptionalSlashRouter()
router.register('customers', CustomersViewSet, base_name="customers")

urlpatterns = []

urlpatterns += router.urls