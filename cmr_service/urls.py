"""cmr_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.staticfiles.urls import static
from django.conf import settings
from django.urls import path, include, re_path

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Customer Service API')
#TODO remove re_path, there's no need for them
urlpatterns = [
    re_path(r'accounts/login/$', LoginView.as_view(template_name='registration/login.html'), name='login'),
    re_path(r'accounts/logout/$', LogoutView.as_view(template_name='registration/login.html'), name='logout'),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    re_path('api/v1/docs/$', schema_view),
    path('api/v1/', include('users.urls')),
    path('api/v1/', include('customers.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
