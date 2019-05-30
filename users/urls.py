from django.urls import re_path

from .routers import OptionalSlashRouter
from .views import UsersViewSet, LoginView


router = OptionalSlashRouter()
router.register('users', UsersViewSet, base_name="users")

urlpatterns = [
    re_path(r'^auth/login\/?$', LoginView.as_view(), name="auth-login")
]

urlpatterns += router.urls