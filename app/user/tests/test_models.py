from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = "teste@email.com"
        password = "test_password"

        user = get_user_model().objects.create_user(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_user_with_invalid_email(self):
        """Test creating a new user with no email raises error"""
        with self.assertRaises(Exception):
            get_user_model().objects.create_user(None, "test_password")

    def test_create_user_unique_email(self):
        """Test creating a new user with email in use raises error"""
        email = "test@email.com"
        get_user_model().objects.create_user(email=email, password="test_password")

        with self.assertRaises(Exception):
            get_user_model().objects.create_user(email=email, password="test_password")

    def test_create_new_superuser(self):
        """Test creating a new user superuser"""
        user = get_user_model().objects.create_superuser(
            "test@email.com", "test_password"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
