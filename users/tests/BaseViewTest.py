from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
import json
from django.contrib.auth import get_user_model


class BaseViewTest(APITestCase):
    client = APIClient()
    User = get_user_model()
    users_limit = 10
    users_ids = {}
    super_user = {'user':'test_super_user', 'pass':'testing'}

    def login_client(self, username="", password=""):
        # Get token
        response = self.client.post(
            reverse('create-token'),
            data=json.dumps(
                {
                    'username': username,
                    'password': password
                }
            ),
            content_type='application/json'
        )
        self.token = response.data['token']
        # Set token in header
        self.client.credentials()
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.token
        )
        self.client.login(username=username, password=password)

    def login_super_user(self):
        self.login_client(BaseViewTest.super_user.get("user"), BaseViewTest.super_user.get("pass"))

    def setUp(self):
        # test admin user
        self.user = self.User.objects.create_superuser(
            username=BaseViewTest.super_user.get("user"),
            email="test@mail.com",
            password=BaseViewTest.super_user.get("pass"),
            first_name="test",
            last_name="user",
        )

        self.login_super_user()

        # test users
        for i in range(0, BaseViewTest.users_limit):
            response = self.client.post(
                reverse("users-list", kwargs={"version": "v1"}),
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