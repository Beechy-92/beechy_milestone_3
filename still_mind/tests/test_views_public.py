from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from still_mind.models import Post


class PostDetailViewPrivateTests(TestCase):
    def setUp(self):
        # Create two users
        self.author = User.objects.create_user(
            username="author", email="author@example.com", password="testpass123"
        )
        self.other_user = User.objects.create_user(
            username="other", email="other@example.com", password="testpass123"
        )

        # Create a draft post owned by 'author'
        self.post = Post.objects.create(
            title="My private post",
            summary="Summary",
            content="Very secret content",
            status=0,  # draft (but in private model, status doesn't affect privacy)
            author=self.author,
            slug="my-private-post",
        )

        self.detail_url = reverse(
            "still_mind:post_detail", kwargs={"slug": self.post.slug}
        )

    def test_author_can_view_own_post_detail(self):
        """Author should see their own post (200)."""
        self.client.login(username="author", password="testpass123")
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "My private post")

    def test_other_user_gets_404_for_post_detail(self):
        """Other logged-in users should see 404 for someone else's post."""
        self.client.login(username="other", password="testpass123")
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 404)

    def test_anonymous_user_redirected_to_login_for_post_detail(self):
        """Anonymous users should be redirected to login."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)
#end of file