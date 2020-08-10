from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
import json
from django.contrib.auth import get_user_model
from oauth2_provider.models import Application


class BaseViewTest(APITestCase):
    client = APIClient()
    User = get_user_model()
    users_limit = 10
    users_ids = {}
    super_user = {'user': 'test_super_user', 'pass': 'testing'}
    app = None

    def login_client(self, username="", password="", get_oauth_token=True):
        self.client.login(username=username, password=password)
        if get_oauth_token:
            self.getOAuthToken(username, password)

    def login_super_user(self):
        self.login_client(BaseViewTest.super_user.get("user"), BaseViewTest.super_user.get("pass"))

    def getOAuthToken(self, username, password):
        response = self.client.post(
            reverse("oauth2_provider:token"),
            data={
                "grant_type": "password",
                "username": self.user.username,
                "password": BaseViewTest.super_user.get("pass"),
                "client_id": self.app.client_id,
                "client_secret": self.app.client_secret
            }
        )
        access_token = response.json()["access_token"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

    def setUp(self):
        # Create super user
        # test super user
        self.user = self.User.objects.create_superuser(
            username=BaseViewTest.super_user.get("user"),
            email="test@mail.com",
            password=BaseViewTest.super_user.get("pass"),
            first_name="test",
            last_name="user",
        )

        self.app = Application.objects.create(user_id=self.user.id,
                                              client_type="confidential",
                                              authorization_grant_type="password",
                                              name="TestApplication")

        self.login_super_user()

        # test users
        for i in range(0, BaseViewTest.users_limit):
            response = self.client.post(
                reverse("users-list"),
                data=json.dumps(
                    {
                        "username": f"User{i}",
                        "password": f"pass{i}",
                        "email": f"new_user{i}@mail.com"
                    }
                ),
                content_type="application/json"
            )
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            BaseViewTest.users_ids.update({f"User{i}": response.data["id"]})
