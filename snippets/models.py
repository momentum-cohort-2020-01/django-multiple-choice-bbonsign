from django.db import models
from django.db.models import CheckConstraint, Q
from django.utils.text import slugify
from users.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=255, help_text='tag or language applied to a snippet')
    langp = models.BooleanField(default=False,
                                 help_text='True if this tag can be used as a language attribute of a snippet')
    slug = models.SlugField(null=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Snippet(models.Model):
    title = models.CharField(max_length=255, blank=True,
                             null=True, help_text='Optional title for the snippet')
    language = models.ForeignKey(
        to=Tag, on_delete=models.SET('no language available'), related_name='code_snippets', help_text='Programming language of the snippet')
    code = models.TextField(help_text='The code of the snippet')
    copies = models.PositiveIntegerField(
        default=0, help_text='Number of times a user has copied the snippet to clipboard')
    tags = models.ManyToManyField(to=Tag, related_name='snippets')
    public = models.BooleanField(
        default=False, help_text='True if the user wants the snippet to be visible to other users')
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE,
                              related_name='snippets', help_text='The user who owns this snippet')
    parent = models.ForeignKey(to='Snippet', on_delete=models.SET_NULL,
                               null=True, blank=True, help_text='The snippet this is forked from')

    def __str__(self):
        return f"{self.owner.id}'s {self.language.name} snippet:{self.id}"
