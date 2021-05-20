import uuid
from django.db import models


class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    author_id = models.ForeignKey("author.Author", on_delete=models.CASCADE)
    category = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    summary = models.TextField()
    first_paragraph = models.TextField(verbose_name="firstParagraph")
    body = models.TextField()

    def __str__(self):
        return self.title
