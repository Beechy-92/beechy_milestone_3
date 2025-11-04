from django.test import TestCase
from django.contrib.auth.models import User
from still_mind.models import Post

class PostModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="testpass")

    def test_default_status_is_draft(self):
        post = Post.objects.create(author=self.user, title="Hello World")
        self.assertEqual(post.status, 0)

    def test_slug_autogenerates_from_title(self):
        post = Post.objects.create(author=self.user, title="My First Post")
        self.assertTrue(post.slug.startswith("my-first-post"))

        