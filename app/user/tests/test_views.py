from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status


SIGNUP_USER_URL = reverse("sign-up")
LOGIN_USER_URL = reverse("login")


class UserViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_signup_user_with_invalid_email_fails(self):
        """Test signup a user with invalid format email fails"""
        payload = dict(
            email="invalid_email",
            password="test_password",
            password_confirmation="test_password",
        )

        response = self.client.post(SIGNUP_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data)

    def test_signup_user_with_email_exists_fails(self):
        """Test signup a user with email is already exists fails"""
        email = "test@email.com"
        get_user_model().objects.create_user(email=email, password="test_password")
        payload = dict(
            email=email, password="test_password", password_confirmation="test_password"
        )

        response = self.client.post(SIGNUP_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data)

    def test_signup_user_with_wrong_passwords_fails(self):
        """Test signup a user with passwords dont match fails"""
        payload = dict(
            email="test@email.com",
            password="test_password",
            password_confirmation="test_wrong_password",
        )

        response = self.client.post(SIGNUP_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data)

    def test_signup_valid_user_successful(self):
        """Test signup a user with valid payload is successful"""
        payload = dict(
            email="test@email.com",
            password="test_password",
            password_confirmation="test_password",
        )

        response = self.client.post(SIGNUP_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], payload["email"])
        self.assertNotIn("password", response.data)

    def test_login_with_invalid_credentials_fails(self):
        """Test login a user with invalid credentials fails"""
        payload = dict(
            email="invalid_email",
            password="",
        )

        response = self.client.post(LOGIN_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data)

    def test_login_not_user_found_fails(self):
        """Test login when not found a user with email provided fails"""
        payload = dict(email="test@email.com", password="test_password")

        response = self.client.post(LOGIN_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data)

    def test_login_wrong_password_fails(self):
        """Test login when password provided is wrong fails"""
        email = "test@email.com"
        get_user_model().objects.create_user(email=email, password="test_password")
        payload = dict(email=email, password="test_wrong_password")

        response = self.client.post(LOGIN_USER_URL, payload)
        user = get_user_model().objects.filter(email=email).first()
        self.assertEqual(email, user.email)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data)

    def test_login_return_token_successful(self):
        """Test login return a token on authenticate successful"""
        email = "test@email.com"
        password = "test_password"
        get_user_model().objects.create_user(email=email, password=password)
        payload = dict(email=email, password=password)

        response = self.client.post(LOGIN_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
