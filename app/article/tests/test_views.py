import uuid
from django.test import TestCase
from django.urls import reverse
from django.apps import apps
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from ..models import Article

AUTHOR_MODEL = apps.get_model("author", "Author")
ADMIN_ARTICLE_URL = reverse("article-admin")


class AdminArticleViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.model = Article
        self.admin = get_user_model().objects.create_superuser(
            email="testadmin@email.com", password="test_password"
        )
        self.author = AUTHOR_MODEL.objects.create(name="Test Author Name")
        self.payload = dict(
            author_id=self.author.id,
            category="Category",
            title="Article title",
            summary="This is a summary of the article",
            first_paragraph="This is the first paragraph of this article",
            body="Second paragraph. Third paragraph",
        )

    def test_login_required(self):
        """Test that login is required for article endpoints"""
        response = self.client.post(ADMIN_ARTICLE_URL, self.payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(response.data)

    def test_admin_level_required(self):
        """Test that admin level is required for article endpoints"""
        user = get_user_model().objects.create_user(
            email="test@email.com", password="test_password"
        )
        self.client.force_authenticate(user=user)

        response = self.client.post(ADMIN_ARTICLE_URL, self.payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(response.data)

    def test_create_article_with_blank_params_fails(self):
        """Test creating article with blank params fails"""
        self.client.force_authenticate(user=self.admin)

        payload = dict(
            author="",
            category="",
            title="",
            summary="",
            first_paragraph="",
            body="",
        )

        response = self.client.post(ADMIN_ARTICLE_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data)

    def test_create_article_with_invalid_author_fails(self):
        """Test creating article with invalid author fails"""
        self.client.force_authenticate(user=self.admin)

        self.payload["author_id"] = "invalid_author"

        response = self.client.post(ADMIN_ARTICLE_URL, self.payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data)

    def test_create_article_with_author_dose_not_exist_fails(self):
        """Test creating article with author dose not exist fails"""
        self.client.force_authenticate(user=self.admin)

        self.payload["author_id"] = uuid.uuid4()

        response = self.client.post(ADMIN_ARTICLE_URL, self.payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data)

    def test_create_article_successful(self):
        """Test creating article successful"""
        self.client.force_authenticate(user=self.admin)

        response = self.client.post(ADMIN_ARTICLE_URL, self.payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["author"]["id"], str(self.payload["author_id"]))
        self.assertEqual(response.data["category"], self.payload["category"])
        self.assertEqual(response.data["title"], self.payload["title"])
        self.assertEqual(response.data["summary"], self.payload["summary"])
        self.assertEqual(
            response.data["first_paragraph"], self.payload["first_paragraph"]
        )
        self.assertEqual(response.data["body"], self.payload["body"])

    def test_update_article_with_invalid_id_fails(self):
        """Test that updating article with id invalid fails"""
        self.client.force_authenticate(user=self.admin)

        self.payload["author_id"] = self.author
        self.model.objects.create(**self.payload)

        self.payload["title"] = "Article new title"
        self.payload["summary"] = "This is a new summary of the article"
        self.payload["author_id"] = self.author.id

        response = self.client.put(f"{ADMIN_ARTICLE_URL}invalid_id", self.payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data)

    def test_update_article_not_found_fails(self):
        """Test that updating article not found fails"""
        self.client.force_authenticate(user=self.admin)

        self.payload["author_id"] = self.author
        self.model.objects.create(**self.payload)

        self.payload["title"] = "Article new title"
        self.payload["summary"] = "This is a new summary of the article"
        self.payload["author_id"] = self.author.id

        response = self.client.put(f"{ADMIN_ARTICLE_URL}{uuid.uuid4()}", self.payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(response.data)

    def test_update_article_successful(self):
        """Test updating article successful"""
        self.client.force_authenticate(user=self.admin)

        self.payload["author_id"] = self.author
        article = self.model.objects.create(**self.payload)

        self.payload["title"] = "Article new title"
        self.payload["summary"] = "This is a new summary of the article"
        self.payload["author_id"] = self.author.id

        response = self.client.put(f"{ADMIN_ARTICLE_URL}{article.id}", self.payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(article.id))
        self.assertEqual(response.data["title"], self.payload["title"])
        self.assertEqual(response.data["summary"], self.payload["summary"])

    def test_remove_article_successful(self):
        """Test that removing article successful"""
        self.client.force_authenticate(user=self.admin)

        self.payload["author_id"] = self.author
        article = self.model.objects.create(**self.payload)

        response = self.client.delete(f"{ADMIN_ARTICLE_URL}{article.id}")
        exists = self.model.objects.filter(id=article.id).exists()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(exists)

    def test_retrieve_article_successful(self):
        """Test that retrieving article successful"""
        self.client.force_authenticate(user=self.admin)

        self.payload["author_id"] = self.author
        article = self.model.objects.create(**self.payload)

        response = self.client.get(f"{ADMIN_ARTICLE_URL}{article.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["author"]["id"], str(article.author_id.id))
        self.assertEqual(response.data["category"], article.category)
        self.assertEqual(response.data["title"], article.title)
        self.assertEqual(response.data["summary"], article.summary)
        self.assertEqual(response.data["first_paragraph"], article.first_paragraph)
        self.assertEqual(response.data["body"], article.body)
