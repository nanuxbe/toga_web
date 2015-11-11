from uuid import uuid4

from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from django.conf import settings
from django.utils.text import slugify


@python_2_unicode_compatible
class CookBook(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    likes = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.name)
        return super(CookBook, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Recipe(models.Model):

    cookbook = models.ForeignKey(CookBook, related_name='recipes')
    title = models.CharField(max_length=500)
    body = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Following(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='follows')
    follows = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='followed_by')
    since = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} followed {} on {}'.format(
            self.user,
            self.follows,
            self.since
        )
