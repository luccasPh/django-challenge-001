from django.test import TestCase

from ..models import Author


class AuthorModelTest(TestCase):
    def setUp(self):
        self.model = Author

    def test_create_author_successful(self):
        """Test creating a new author successful"""
        data = dict(name="Test Author Name")

        author = self.model.objects.create(**data)
        self.assertEqual(author.name, "Test Author Name")
        self.assertFalse(author.picture)

    def test_update_author_successful(self):
        """Test updating an author successful"""
        create_data = dict(name="Test Author Name")
        update_data = dict(name="Test Author Name", picture="test_picture_name")
        user = self.model.objects.create(**create_data)

        self.model.objects.filter(id=user.id).update(**update_data)
        user.refresh_from_db()
        self.assertEqual(user.name, update_data["name"])
        self.assertEqual(user.picture, update_data["picture"])

    def test_retrieve_an_author_successful(self):
        """Test retrieving an author successful"""
        data = dict(name="Test Author Name")
        create_user = self.model.objects.create(**data)

        retrieve_user = self.model.objects.filter(id=create_user.id).first()
        self.assertEqual(retrieve_user.id, create_user.id)
        self.assertEqual(retrieve_user.name, create_user.name)

    def test_remove_an_author_successful(self):
        """Test removing an author successful"""
        data = dict(name="Test Author Name")
        user = Author.objects.create(**data)
        self.model.objects.filter(id=user.id).delete()

        self.assertFalse(self.model.objects.filter(id=user.id).exists())
