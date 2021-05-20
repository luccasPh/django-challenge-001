from django.test import TestCase
from django.apps import apps

from ..models import Article

AUTHOR_MODEL = apps.get_model("author", "Author")


class ArticleModelTest(TestCase):
    def setUp(self):
        self.model = Article
        self.author = AUTHOR_MODEL.objects.create(name="Test Author Name")

    def test_create_article_successful(self):
        """Test creating a new article successful"""
        data = dict(
            author_id=self.author,
            category="Category",
            title="Article title",
            summary="This is a summary of the article",
            firstParagraph="This is the first paragraph of this article",
            body="Second paragraph. Third paragraph",
        )

        article = self.model.objects.create(**data)
        self.assertTrue(article.id)
        self.assertEqual(article.author_id, self.author)
        self.assertEqual(article.category, data["category"])
        self.assertEqual(article.title, data["title"])
        self.assertEqual(article.summary, data["summary"])
        self.assertEqual(article.firstParagraph, data["firstParagraph"])
        self.assertEqual(article.body, data["body"])

    def test_update_article_successful(self):
        """Test updating an article successful"""
        create_data = dict(
            author_id=self.author,
            category="Category",
            title="Article title",
            summary="This is a summary of the article",
            firstParagraph="This is the first paragraph of this article",
            body="Second paragraph. Third paragraph",
        )
        article = self.model.objects.create(**create_data)

        update_data = dict(
            author_id=self.author,
            category="New Category",
            title="Article new title",
            summary="This is a new summary of the article",
            firstParagraph="This is the new first paragraph of this article",
            body="Second new paragraph. Third new paragraph",
        )
        self.model.objects.filter(id=article.id).update(**update_data)
        article.refresh_from_db()
        self.assertEqual(article.author_id, update_data["author_id"])
        self.assertEqual(article.category, update_data["category"])
        self.assertEqual(article.title, update_data["title"])
        self.assertEqual(article.summary, update_data["summary"])
        self.assertEqual(article.firstParagraph, update_data["firstParagraph"])
        self.assertEqual(article.body, update_data["body"])

    def test_retrieve_an_article_successful(self):
        """Test retrieving an article successful"""
        data = dict(
            author_id=self.author,
            category="Category",
            title="Article title",
            summary="This is a summary of the article",
            firstParagraph="This is the first paragraph of this article",
            body="Second paragraph. Third paragraph",
        )
        article = self.model.objects.create(**data)

        retrieve_article = self.model.objects.filter(id=article.id).first()
        self.assertEqual(retrieve_article.id, article.id)
        self.assertEqual(retrieve_article.author_id, article.author_id)
        self.assertEqual(retrieve_article.category, article.category)
        self.assertEqual(retrieve_article.title, article.title)
        self.assertEqual(retrieve_article.summary, article.summary)
        self.assertEqual(retrieve_article.firstParagraph, article.firstParagraph)
        self.assertEqual(retrieve_article.body, article.body)

    def test_remove_an_article_successful(self):
        """Test removing an article successful"""
        data = dict(
            author_id=self.author,
            category="Category",
            title="Article title",
            summary="This is a summary of the article",
            firstParagraph="This is the first paragraph of this article",
            body="Second paragraph. Third paragraph",
        )
        article = self.model.objects.create(**data)

        self.model.objects.filter(id=article.id).delete()
        exists = self.model.objects.filter(id=article.id).exists()
        self.assertFalse(exists)
