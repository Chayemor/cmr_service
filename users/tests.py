from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
import json
from django.contrib.auth import get_user_model

from .serializer import UserSerializer


# python manage.py test users.tests.AuthRegisterUserTest.test_register_user_with_valid_data

class BaseViewTest(APITestCase):
    client = APIClient()
    User = get_user_model()
    users_limit = 100

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
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.token
        )
        self.client.login(username=username, password=password)
        return self.token

    @staticmethod
    def create_super_user(name="", password=""):
        if name != "" and password != "":
            get_user_model().objects.create(
                username=name,
                password=password)

    @staticmethod
    def create_user(name="", password=""):
        if name != "" and password != "":
            get_user_model().objects.create(
                username=name,
                password=password)

    def login_super_user(self):
        self.login_client('test_super_user', 'testing')

    def login_a_user(self, username="", password=""):
        url = reverse(
            "auth-login",
            kwargs={
                "version": "v1"
            }
        )
        return self.client.post(
            url,
            data=json.dumps({
                "username": username,
                "password": password
            }),
            content_type="application/json"
        )

    def setUp(self):
        # test admin user
        self.user = self.User.objects.create_superuser(
            username="test_super_user",
            email="test@mail.com",
            password="testing",
            first_name="test",
            last_name="user",
        )

        # test users
        for i in range(0, BaseViewTest.users_limit):
            self.create_user(f"User{i}", f"pass{i}")


class UsersTest(BaseViewTest):
    @staticmethod
    def get_users_api():
        return reverse(f"users-list", kwargs={"version": "v1"})

    def test_admin_access(self):
        url = UsersTest.get_users_api()
        self.login_a_user("User0", "pass0")

        # 401 Unauthorized
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_users(self):
        """
        Users added in the setUp method exist
        """
        self.login_super_user()
        response = self.client.get(UsersTest.get_users_api())
        # db data
        expected = self.User.objects.all()
        serialized = UserSerializer(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_user_with_valid_data(self):
        url = UsersTest.get_users_api()
        self.login_super_user()

        # code must be 201 Created
        response = self.client.post(
            url,
            data=json.dumps(
                {
                    "username": "new_user",
                    "password": "new_pass",
                    "email": "new_user@mail.com"
                }
            ),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # code must be 201 Created, email is not required
        response = self.client.post(
            url,
            data=json.dumps(
                {
                    "username": "new_user_2",
                    "password": "new_pass"
                }
            ),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #code must be 400 Bad Request, user already exists
        response = self.client.post(
            url,
            data=json.dumps(
                {
                    "username": "new_user_2",
                    "password": "new_pass"
                }
            ),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_user_with_invalid_data(self):
        url = UsersTest.get_users_api()
        self.login_super_user()
        response = self.client.post(
            url,
            data=json.dumps(
                {
                    "username": "",
                    "password": "",
                    "email": ""
                }
            ),
            content_type='application/json'
        )
        # code must be 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.post(
            url,
            data=json.dumps(
                {
                    "username": "",
                    "email": ""
                }
            ),
            content_type='application/json'
        )
        # code must be 400 Bad Request, password is mandatory
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_user(self):
        self.login_super_user()
        user_id = "1"
        # Toggle user's admin status
        response = self.client.get(f"{UsersTest.get_users_api()}/{user_id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.patch(
            f"{UsersTest.get_users_api()}/{user_id}",
            data=json.dumps({"is_admin": "True"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.get("is_admin"))
        # Toggle back
        response = self.client.patch(
            f"{UsersTest.get_users_api()}/{user_id}",
            data=json.dumps({"is_admin": "False"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data.get("is_admin"))

    def test_put_user(self):
        self.login_super_user()
        user_id = "1"
        # Try put with optional field only
        response = self.client.get(f"{UsersTest.get_users_api()}/{user_id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put(
            f"{UsersTest.get_users_api()}/{user_id}",
            data=json.dumps({"email": "ss@gmail.com"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



class AuthLoginUserTest(BaseViewTest):
    """
    Tests for the auth/login/ endpoint
    """

    def test_login_user(self):
        # valid credentials, code is 200 OK and token is in response.data
        response = self.login_a_user('test_super_user', 'testing')
        self.assertIn("token", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # invalid credentials, 401 UNAUTHORIZED
        response = self.login_a_user("anonymous", "pass")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
