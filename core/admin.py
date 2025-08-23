from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_on")
    list_filter = ("created_on",)
    search_fields = ("title", "author", "content")
    prepopulated_fields = {"slug": ("title",)}
