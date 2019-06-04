from .routers import OptionalSlashRouter
from .views import UsersViewSet


router = OptionalSlashRouter()
router.register('users', UsersViewSet, base_name="users")

urlpatterns = []

urlpatterns += router.urls