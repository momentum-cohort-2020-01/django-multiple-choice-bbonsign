from django.contrib import admin

from .models import Tag, Snippet


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Tag, TagAdmin)
admin.site.register(Snippet)
