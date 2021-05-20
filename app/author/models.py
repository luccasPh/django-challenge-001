import uuid
import os
from django.db import models


def author_picture_file_name(instance, filename):
    new_filename = f"{uuid.uuid4()}-{filename}"
    return os.path.join("pictures/", new_filename)


class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    picture = models.ImageField(
        null=True, default=None, upload_to=author_picture_file_name
    )

    def __str__(self):
        return self.name
