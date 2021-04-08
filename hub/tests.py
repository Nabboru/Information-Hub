from django.test import TestCase
from .models import Post
from accounts.models import User


class PostTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(
            'professional',
            email='test@test.com',
            password='test123',
            first_name='Professional',
            last_name='Testing',
            is_professional=True
        )
        user1.save()

        user2 = User.objects.create_user(
            'patient',
            email='patient@test.com',
            password='test123',
            first_name='Patient',
            last_name='Testing',
            is_professional=False
        )
        user2.save()

        post = Post(title="test title", content="test content", author=user1)
        post.save()

    def test_post_created(self):
        post = Post.objects.get(pk=1)
        user1 = User.objects.get(pk=1)
        user2 = User.objects.get(pk=2)
        self.assertEqual(post.title, "test title")
        self.assertEqual(post.content, "test content")
        self.assertEqual(post.author, user1)
        self.assertNotEqual(post.title, "fake title")
        self.assertNotEqual(post.content, "fake content")
        self.assertNotEqual(post.author, user2)

    def test_post_edited(self):
        post = Post.objects.get(pk=1)
        user = User.objects.get(pk=1)
        post.title = "edited title"
        post.content = "edited content"
        self.assertEqual(post.title, "edited title")
        self.assertEqual(post.content, "edited content")
        self.assertEqual(post.author, user)
        self.assertNotEqual(post.title, "test title")
        self.assertNotEqual(post.content, "test content")

    def test_post_deleted(self):
        post = Post.objects.get(pk=1)
        user = User.objects.get(pk=1)
        post.delete()
        post_count = Post.objects.all().count()
        self.assertEqual(post_count, 0)

