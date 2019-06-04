from django.urls import reverse
#from django.contrib.auth import get_user_model
import json

#from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from PIL import Image
import tempfile

from users.tests.BaseViewTest import BaseViewTest

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
                    "name": "pass"
                }
            ),
            content_type="application/json"
        )
        # 201 created, required fields have been supplied
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["created_by"]["username"], BaseViewTest.super_user.get("user"))
        self.assertEqual(response.data["modified_by"]["username"], BaseViewTest.super_user.get("user"))

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
        self.login_client("User0", "pass0")

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
            self.assertEqual(response.data["created_by"]["username"], BaseViewTest.super_user.get("user"))
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
            self.assertEqual(response.data["created_by"]["username"], BaseViewTest.super_user.get("user"))
            self.assertEqual(response.data["modified_by"]["username"], "User0")

        # DELETE customer
        response = self.client.delete(url, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_crud_customer_diff_users(self):
        url = self.get_customers_api()
        self.login_client("User0", "pass0")

        # create customer
        response = self.client.post(
            url,
            data=json.dumps(
                {
                    "surname": "new_user",
                    "name": "pass"
                }
            ),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_customer_id = response.data["id"]

        # patch customer with different user
        url = f"{url}/{new_customer_id}"
        self.login_client("User2", "pass2")
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


