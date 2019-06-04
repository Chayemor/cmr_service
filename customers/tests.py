from django.urls import reverse
from django.contrib.auth import get_user_model
import json
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from PIL import Image
import tempfile

class BaseViewTest(APITestCase):
    client = APIClient()

    client = APIClient()
    User = get_user_model()
    users_limit = 8
    users_ids = {}
    super_user = 'test_super_user'

    def login_super_user(self):
        self.login_token(BaseViewTest.super_user, 'testing')

    def login_token(self, username="", password=""):
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

    def setUp(self):
        # test admin user
        self.user = self.User.objects.create_superuser(
            username="test_super_user",
            email="test@mail.com",
            password="testing",
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
                        "password": f"new_pass{i}",
                        "email": f"new_user{i}@mail.com"
                    }
                ),
                content_type="application/json"
            )
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            BaseViewTest.users_ids.update({f"User{i}" : response.data["id"]})

class CustomersTest(BaseViewTest):
    @staticmethod
    def get_customers_api():
        return reverse("customers-list", kwargs={"version": "v1"})

    @staticmethod
    def get_image(prefix, suffix):
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(prefix=prefix, suffix=f".{suffix}")
        image.save(tmp_file)
        return tmp_file

    def compare_photo(self, photo, against):
        self.assertEqual(photo.split("/")[-1], against.split("/")[-1])

    def test_customer_creation(self):
        url = self.get_customers_api()
        self.login_super_user()

        response = self.client.post(
            url,
            data=json.dumps(
                {
                    "surname": "new_user",
                    "name": "new_pass"
                }
            ),
            content_type="application/json"
        )
        # 201 created, required fields have been supplied
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["created_by"]["username"], BaseViewTest.super_user)
        self.assertEqual(response.data["modified_by"]["username"], BaseViewTest.super_user)

        # code must be 400 Bad Request, name is required
        response = self.client.post(
            url,
            data=json.dumps({"surname": "new_user_2"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Create tmp image
        tmp_file = CustomersTest.get_image("test", "jpg")
        with open(tmp_file.name, 'rb') as data:
            response = self.client.post(url,
                                        {"name": "hello",
                                         "surname": "It's me",
                                         "photo": data},
                                        format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.compare_photo(response.data["photo"], tmp_file.name)

    def test_rud_customer(self):
        url = self.get_customers_api()
        self.login_super_user()

        tmp_file = CustomersTest.get_image("test", "jpg")
        with open(tmp_file.name, 'rb') as data:
            response = self.client.post(url,
                                        {"name": "hello",
                                         "surname": "It's me",
                                         "photo": data},
                                        format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            new_customer_id = response.data["id"]

        url = f"{url}/{new_customer_id}"
        self.login_token("User0", "new_pass0")

        # PATCH customer
        tmp_file = CustomersTest.get_image("newtest", "png")
        with open(tmp_file.name, 'rb') as data:
            response = self.client.patch(url,
                                        {"surname": "It's me again",
                                         "photo": data},
                                        format='multipart')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.compare_photo(response.data["photo"], tmp_file.name)
            self.assertEqual(response.data["surname"], "It's me again")
            self.assertEqual(response.data["created_by"]["username"], BaseViewTest.super_user)
            self.assertEqual(response.data["modified_by"]["username"], "User0")

        # PUT customer
        tmp_file = CustomersTest.get_image("newest", "jpeg")
        with open(tmp_file.name, 'rb') as data:
            response = self.client.put(url,
                                         {"surname": "It's me again",
                                          "photo": data},
                                         format='multipart')
            # name is mandatory
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        tmp_file = CustomersTest.get_image("newest", "jpeg")
        with open(tmp_file.name, 'rb') as data:
            response = self.client.put(url,
                                       {"surname": "It's me again again",
                                        "name": "Hello",
                                        "photo": data},
                                       format='multipart')
            # name is mandatory
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.compare_photo(response.data["photo"], tmp_file.name)
            self.assertEqual(response.data["surname"], "It's me again again")
            self.assertEqual(response.data["created_by"]["username"], BaseViewTest.super_user)
            self.assertEqual(response.data["modified_by"]["username"], "User0")

        # DELETE customer
        response = self.client.delete(url, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_crud_customer_diff_users(self):
        url = self.get_customers_api()
        self.login_token("User0", "new_pass0")

        # create customer
        response = self.client.post(
            url,
            data=json.dumps(
                {
                    "surname": "new_user",
                    "name": "new_pass"
                }
            ),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_customer_id = response.data["id"]

        # patch customer with different user
        url = f"{url}/{new_customer_id}"
        self.login_token("User2", "new_pass2")
        tmp_file = CustomersTest.get_image("newtest", "png")
        with open(tmp_file.name, 'rb') as data:
            response = self.client.patch(url,
                                         {"photo": data},
                                         format='multipart')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.compare_photo(response.data["photo"], tmp_file.name)
            self.assertEqual(response.data["created_by"]["username"], "User0")
            self.assertEqual(response.data["modified_by"]["username"], "User2")

        # Delete one of the users
        self.login_super_user()
        url = reverse(f"users-list", kwargs={"version": "v1"})
        url = f"{url}/{self.users_ids['User0']}"
        response = self.client.delete(url, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        url = self.get_customers_api()
        url = f"{url}/{new_customer_id}"
        response = self.client.get(url, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["created_by"], None)
        self.assertEqual(response.data["modified_by"]["username"], "User2")


