# Generated by Django 3.1.5 on 2021-05-20 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='author',
            new_name='author_id',
        ),
    ]
