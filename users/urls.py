from .routers import OptionalSlashRouter
from .views import UsersViewSet


router = OptionalSlashRouter()
router.register('users', UsersViewSet, basename="users")

urlpatterns = []

urlpatterns += router.urls
