from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory


class TestRegister(TestCase):
    """
    Tests the registration function.
    """

    client = APIRequestFactory()
    registration_url = reverse("user:RegisterView")

    def test_invalid_username_creation_0(self):
        response = self.client.post(self.registration_url, {
            "username": "new_user",
            "password": "password"
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_username_creation_1(self):
        response = self.client.post(self.registration_url, {
            "username": "new.user",
            "password": "password"
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_user_creation_0(self):
        response = self.client.post(self.registration_url, {
            "username": "newuser",
            "password": "password"
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_valid_username_creation_1(self):
        response = self.client.post(self.registration_url, {
            "username": "newuser1",
            "password": "password"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_valid_username_creation_2(self):
        response = self.client.post(self.registration_url, {
            "username": "11111111111",
            "password": "password"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestUserLogin(TestCase):
    """
    Tests user logging in.
    """

    USERNAME = "testuser2"
    PASSWORD = "testuser2"

    login_url = reverse("user:GetRefreshToken")
    client = APIRequestFactory()

    def setUp(self) -> None:
        get_user_model().objects.create_user(username=self.USERNAME, password=self.PASSWORD)

    def test_successful_login(self):
        response_data = self.client.post(
            self.login_url,
            {"username": self.USERNAME, "password": self.PASSWORD},
        )

        self.assertEqual(response_data.status_code, status.HTTP_200_OK)

    def test_invalid_credential_login(self):
        response_data = self.client.post(
            self.login_url,
            {"username": self.USERNAME + "random", "password": self.PASSWORD},
        )

        self.assertEqual(response_data.status_code, status.HTTP_401_UNAUTHORIZED)


class TestGetAccessTokenView(TestCase):
    """
    Tests user trying to get Access Token
    """

    USERNAME = "testuser2"
    PASSWORD = "testuser2"

    login_url = reverse("user:GetRefreshToken")
    access_token_url = reverse("user:GetAccessToken")
    refresh_token = None
    client = APIRequestFactory()

    def setUp(self) -> None:
        get_user_model().objects.create_user(username=self.USERNAME, password=self.PASSWORD)
        response = self.client.post(
            self.login_url, {
                "username": self.USERNAME,
                "password": self.PASSWORD
            }
        )
        self.refresh_token = response.data.get('refresh')

    def test_successful_access_token(self):
        response = self.client.post(
            self.access_token_url, {
                "refresh": self.refresh_token
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unsuccessful_access_token(self):
        response = self.client.post(
            self.access_token_url, {
                "refresh": self.refresh_token + "random"
            }
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserManagerTestCase(TestCase):
    """
    Tests `user.Managers.UserManager`
    """

    User = get_user_model()
    test_username = "testUser1"
    test_password = "99999999"

    def test_create_user(self) -> None:
        user = self.User.objects.create_user(username=self.test_username, password=self.test_password)

        try:
            self.assertIsNotNone(user.id, "User not created.")
            self.assertEqual(self.test_username, user.username)

            self.assertTrue(user.is_active)
            self.assertFalse(user.is_staff)
            self.assertFalse(user.is_superuser)

            self.assertIsNone(getattr(user, "email", None))

            with self.assertRaises(TypeError):
                self.User.objects.create_user()
            with self.assertRaises(TypeError):
                self.User.objects.create_user(username='')
            with self.assertRaises(ValueError):
                self.User.objects.create_user(username='', password=self.test_password)
        finally:
            user.delete()

    def test_create_superuser(self) -> None:
        user = self.User.objects.create_superuser(username=self.test_username, password=self.test_password)

        try:
            self.assertIsNotNone(user.id, "User not created.")
            self.assertEqual(self.test_username, user.username)

            self.assertTrue(user.is_active)
            self.assertTrue(user.is_staff)
            self.assertTrue(user.is_superuser)

            self.assertIsNone(getattr(user, "email", None))

            with self.assertRaises(TypeError):
                self.User.objects.create_superuser()
            with self.assertRaises(TypeError):
                self.User.objects.create_superuser(username='')
            with self.assertRaises(ValueError):
                self.User.objects.create_superuser(username='', password=self.test_password)
        finally:
            user.delete()
