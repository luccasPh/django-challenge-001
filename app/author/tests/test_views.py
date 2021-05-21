import os
import uuid
import tempfile
from PIL import Image
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.test import APIClient
from rest_framework import status

from ..models import Author

AUTHOR_URL = reverse("authors")


def remove_file(filename):
    os.remove(settings.MEDIA_ROOT.joinpath(filename))


class AuthorViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.model = Author
        self.admin = get_user_model().objects.create_superuser(
            email="testadmin@email.com", password="test_password"
        )

    def test_login_required(self):
        """Test that login is required for author endpoint"""
        payload = dict(name="Test Author Name")

        response = self.client.post(AUTHOR_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(response.data)

    def test_admin_level_required(self):
        """Test that admin level is required for author endpoint"""
        payload = dict(name="Test Author Name")
        user = get_user_model().objects.create_user(
            email="test@email.com", password="test_password"
        )
        self.client.force_authenticate(user=user)

        response = self.client.post(AUTHOR_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(response.data)

    def test_create_author_without_name_fails(self):
        """Test creating author without name fails"""
        self.client.force_authenticate(user=self.admin)

        payload = dict(name="")

        response = self.client.post(AUTHOR_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data)

    def test_create_author_successful(self):
        """Test creating author successful"""
        self.client.force_authenticate(user=self.admin)

        payload = dict(name="Test Author Name")

        response = self.client.post(AUTHOR_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], payload["name"])

    def test_update_author_with_invalid_id_fails(self):
        """Test that updating author with id invalid fails"""
        self.client.force_authenticate(user=self.admin)

        payload = dict(name="Test Author New Name")

        response = self.client.put(f"{AUTHOR_URL}invalid_id/", payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data)

    def test_update_author_not_found_fails(self):
        """Test that updating author not found fails"""
        self.client.force_authenticate(user=self.admin)

        payload = dict(name="Test Author New Name")

        response = self.client.put(f"{AUTHOR_URL}{uuid.uuid4()}/", payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(response.data)

    def test_update_author_successful(self):
        """Test that updating author successful"""
        self.client.force_authenticate(user=self.admin)

        author = self.model.objects.create(name="Test Author Name")
        payload = dict(name="Test Author New Name")

        response = self.client.put(f"{AUTHOR_URL}{author.id}/", payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], payload["name"])

    def test_remove_author_successful(self):
        """Test that removing author successful"""
        self.client.force_authenticate(user=self.admin)

        author = self.model.objects.create(name="Test Author Name")

        response = self.client.delete(f"{AUTHOR_URL}{author.id}/")
        author = self.model.objects.filter(id=author.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(author)

    def test_author_upload_picture_successful(self):
        """Test that uploading picture for author successful"""
        self.client.force_authenticate(user=self.admin)

        author = self.model.objects.create(name="Test Author Name")
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            response = self.client.patch(
                f"{AUTHOR_URL}{author.id}/picture/",
                dict(picture=ntf),
                format="multipart",
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["picture"])

        author.refresh_from_db()
        remove_file(f"{author.picture}")

    def test_retrieve_author_successful(self):
        """Test that retrieving author successful"""
        self.client.force_authenticate(user=self.admin)

        author = self.model.objects.create(name="Test Author Name")

        response = self.client.get(f"{AUTHOR_URL}{author.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(author.id))
        self.assertEqual(response.data["name"], author.name)
        self.assertEqual(response.data["picture"], author.picture)
