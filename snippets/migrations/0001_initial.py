# Generated by Django 3.0.4 on 2020-03-10 02:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='tag language applied to a snippet', max_length=255)),
                ('slug', models.SlugField(null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='tag language applied to a snippet', max_length=255)),
                ('slug', models.SlugField(null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Snippet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, help_text='Optional title for the snippet', max_length=255, null=True)),
                ('code', models.TextField(help_text='The code of the snippet')),
                ('copies', models.PositiveIntegerField(default=0, help_text='Number of times a user has copied the snippet to clipboard')),
                ('public', models.BooleanField(default=False, help_text='True if the user wants the snippet to be visible to other users')),
                ('language', models.ForeignKey(help_text='Programming language of the snippet', on_delete=models.SET('no language available'), related_name='snippets', to='snippets.Language')),
                ('owner', models.ForeignKey(help_text='The user who owns this snippet', on_delete=django.db.models.deletion.CASCADE, related_name='snippets', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, help_text='The snippet this is forked from', null=True, on_delete=django.db.models.deletion.SET_NULL, to='snippets.Snippet')),
                ('tags', models.ManyToManyField(related_name='snippets', to='snippets.Tag')),
            ],
        ),
    ]
