from django.db import models
# from django.db.models import CheckConstraint, Q
from django.utils.text import slugify
from users.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=255, help_text='tag language applied to a snippet')
    slug = models.SlugField(null=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=255,
                            help_text='tag language applied to a snippet')
    slug = models.SlugField(null=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Snippet(models.Model):
    title = models.CharField(max_length=255, blank=True,
                             null=True,
                             help_text='Optional title for the snippet')
    language = models.ForeignKey(to=Language,
                                 on_delete=models.SET('no language available'),
                                 related_name='snippets',
                                 help_text='Programming language of the snippet')
    code = models.TextField(help_text='The code of the snippet')
    description = models.TextField(help_text='Optional description of the code',
                            blank=True, null=True)
    copies = models.PositiveIntegerField(default=0,
                                         help_text='Number of times a user has copied the snippet to clipboard')
    tags = models.ManyToManyField(to=Tag, related_name='snippets', blank=True)
    public = models.BooleanField(default=False,
                                 help_text='True if the user wants the snippet to be visible to other users')
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,
                              related_name='snippets',
                              help_text='The user who owns this snippet')
    parent = models.ForeignKey(to='Snippet', on_delete=models.SET_NULL,
                               related_name='children',
                               null=True, blank=True,
                               help_text='The snippet this is forked from')

    def __str__(self):
        return f"{self.owner.id}'s {self.language.name} snippet:{self.id}"

    @property
    def preview(self):
        limit = 15
        count = 0
        code = self.code
        preview = ''
        for char in code:
            if char == '\n':
                count += 1
            if count < limit:
                preview += char
        return preview
