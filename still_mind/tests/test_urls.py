from django.test import SimpleTestCase
from django.urls import reverse, resolve
from still_mind.views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)

class TestUrls(SimpleTestCase):
    def test_post_list_url_resolves(self):
        url = reverse("still_mind:post_list")
        self.assertEqual(resolve(url).func.view_class, PostListView)

    def test_post_detail_url_resolves(self):
        url = reverse("still_mind:post_detail", args=["sample-slug"])
        self.assertEqual(resolve(url).func.view_class, PostDetailView)

    def test_post_create_resolves(self):
        url = reverse("still_mind:post_create")
        self.assertEqual(resolve(url).func.view_class, PostCreateView)

    def test_post_edit_url_resolves(self):
        url = reverse("still_mind:post_edit", kwargs={"slug": "example-slug"})
        self.assertEqual(resolve(url).func.view_class, PostUpdateView)

    def test_post_delete_url_resolves(self):
        url = reverse("still_mind:post_delete", kwargs={"slug": "example-slug"})
        self.assertEqual(resolve(url).func.view_class, PostDeleteView)

# newline at end of file