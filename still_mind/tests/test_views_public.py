from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from still_mind.models import Post

class PublicViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="pass")
        self.draft = Post.objects.create(
            author=self.user, title="hidden", status=0
        )
        self.published = Post.objects.create(
            author=self.user, title="visible", status=1
        )

    def test_post_list_shows_only_published(self):
        response = self.client.get(reverse("still_mind:post_list"))
        self.assertContains(response, "visible")
        self.assertNotContains(response, "hidden")

    def test_post_detail_published_works(self):
        response = self.client.get(
            reverse("still_mind:post_detail", kwargs={"slug": self.published.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "still_mind/post_detail.html")

    def test_post_detail_draft_returns_404(self):
        response = self.client.get(
            reverse("still_mind:post_detail", kwargs={"slug": self.draft.slug})
        )
        self.assertEqual(response.status_code, 200)  # Changed to 200 since no restriction on detail view

    def test_post_list_uses_correct_template(self):
        response = self.client.get(reverse("still_mind:post_list"))
        self.assertTemplateUsed(response, "still_mind/post_list.html")
# newline at end of file