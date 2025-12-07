from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from itertools import count

# Create your models here.

STATUS = (
    (0, "Draft"),
    (1, "Published")   
)


class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    title = models.CharField(max_length=200) 
    slug = models.SlugField(max_length=200, blank=True) # will be set in save()
    mood = models.CharField(max_length=50, blank=True)
    summary = models.CharField(max_length=280, blank=True)
    content = models.TextField(blank=True)
    status = models.IntegerField(choices=STATUS, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Unique slug **per author**
        constraints = [
            models.UniqueConstraint(fields=["author", "slug"], name="unique_author_slug"),
        ]
        # Helpful indexes for lookups
        indexes = [
            models.Index(fields=["author", "slug"]),
            models.Index(fields=["slug"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} — {self.author.username}"

    def get_absolute_url(self):
        
        return reverse("still_mind:post_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        """
        Auto-generate a unique slug per author.
        """
        if not self.slug:
            base = slugify(self.title) or "post"
            base = base[:180]
            candidate = base

            for i in count(2):
                qs = Post.objects.filter(author=self.author, slug=candidate)
                if self.pk:
                    qs = qs.exclude(pk=self.pk)
                if not qs.exists():
                    break
                candidate = f"{base}-{i}"
                candidate = candidate[:200]

            self.slug = candidate

        super().save(*args, **kwargs)
