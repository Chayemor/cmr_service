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
from django.urls import path, include, re_path

from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Customer Service API')

urlpatterns = [
    re_path(r'accounts/login/$', LoginView.as_view(template_name='registration/login.html'), name='login'),
    re_path(r'accounts/logout/$', LogoutView.as_view(template_name='registration/login.html'), name='logout'),
    path('api-token-auth', obtain_jwt_token, name='create-token'),
    re_path('api/v1/docs/$', schema_view),
    re_path('api/v1/', include('users.urls')),
    re_path('api/v1/', include('customers.urls')),
]