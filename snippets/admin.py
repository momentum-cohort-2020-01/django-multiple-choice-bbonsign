from django.contrib import admin

from .models import Tag, Snippet, Language


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class LanguageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Tag, TagAdmin)
admin.site.register(Snippet)
admin.site.register(Language, LanguageAdmin)
