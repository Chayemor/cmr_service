from django.urls import reverse
#from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
import json
#from django.contrib.auth import get_user_model

from ..serializer import UserSerializer
from .BaseViewTest import BaseViewTest


# python manage.py test users.tests.AuthRegisterUserTest.test_register_user_with_valid_data

class UsersTest(BaseViewTest):
    @staticmethod
    def get_users_api():
        return reverse(f"users-list")

    def test_admin_access(self):
        url = UsersTest.get_users_api()
        self.login_client("User0", "pass0")

        # 403 Forbidden
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Change to admin status and try again
        self.login_super_user()
        user_id = self.users_ids.get("User0")
        # Toggle user's admin status
        response = self.client.get(f"{url}/{user_id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.patch(
            f"{UsersTest.get_users_api()}/{user_id}",
            data=json.dumps({"is_admin": "True"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.get("is_admin"))

        # 200 ok
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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
        user_id = self.users_ids.get("User0")
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
        user_id = self.users_ids.get("User5")
        # Try put with optional field only
        response = self.client.get(f"{UsersTest.get_users_api()}/{user_id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put(
            f"{UsersTest.get_users_api()}/{user_id}",
            data=json.dumps({"email": "ss@gmail.com"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

