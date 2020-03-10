import json
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from snippets.models import Language


class Command(BaseCommand):
    help = 'Import all support Prism.js languages into db as Language instances'

    def handle(self, *args, **kwargs):
        with open('prism_langs.json', 'r') as f:
            langs = json.load(f)
        languages = langs['languages']
        lang_list = []
        slug_list = []

        for value in languages.values():
            lang = value['title']
            slug = slugify(lang)
            if slug not in slug_list:
                slug_list.append(slug)
                lang_list.append(lang)
            aliases = value.get('aliasTitles')
            if aliases is not None:
                for lang in aliases.values():
                    slug= slugify(lang)
                    if slugify(lang) not in slug_list:
                        slug_list.append(slug)
                        lang_list.append(lang)

        for lang in lang_list:
            _, created = Language.objects.get_or_create(name=lang)
