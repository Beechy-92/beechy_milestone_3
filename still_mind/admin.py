from django.contrib import admin
from .models import Post

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "mood", "created_at")
    list_filter = ("status", "mood", "created_at", "author")
    search_fields = ("title", "summary", "content", "author__username")
    ordering = ("-created_at",)
    prepopulated_fields = {"slug": ("title",)}
