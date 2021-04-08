from forum.models import ForumPost, Comment, AnnouncementPost
from accounts.models import User
from django.test import TestCase

class ForumPostTest(TestCase):
    def setUp(self):
        user_email = 'testing@email.com'
        test_user = User.objects.create_user(username= 'test', email= user_email, password = 'testing@123')
        test_user.save()
        ForumPost.objects.create(username = test_user, subject="Test1", content="Test1 content", for_patient=False, for_family=False)
        ForumPost.objects.create(username = test_user, subject="Test2", content="Test2 content", for_patient=False, for_family=False)
        ForumPost.objects.create(username = test_user, subject="Test3", content="Test3 content", for_patient=True, for_family=False)

    def test_post_subject(self):
        test1 = ForumPost.objects.get(subject="Test1")
        test2 = ForumPost.objects.get(subject="Test2")
        test3 = ForumPost.objects.get(subject="Test3")
        self.assertEqual(test1.subject, 'Test1')
        self.assertEqual(test2.subject, 'Test2')
        self.assertEqual(test3.subject, 'Test3')

class AnnouncementPostTest(TestCase):
    def setUp(self):
        AnnouncementPost.objects.create(subject="Test1", content="Test1 content")
        AnnouncementPost.objects.create(subject="Test2", content="Test2 content")
        AnnouncementPost.objects.create(subject="Test3", content="Test3 content")

    def test_announcement_post_subject(self):
        test1 = AnnouncementPost.objects.get(subject="Test1")
        test2 = AnnouncementPost.objects.get(subject="Test2")
        test3 = AnnouncementPost.objects.get(subject="Test3")
        self.assertEqual(test1.subject, 'Test1')
        self.assertEqual(test2.subject, 'Test2')
        self.assertEqual(test3.subject, 'Test3')

class CommentTest(TestCase):
    def setUp(self):

        user_email = 'testing@email.com'
        test_user = User.objects.create_user(username= 'test', email= user_email, password = 'testing@123')
        test_user.save()
        post = ForumPost.objects.create(username = test_user, subject="Test1", content="Test1 content", for_patient=False, for_family=False)
        Comment.objects.create(username = test_user, post_id = post.id, content="Test1 content")
        Comment.objects.create(username = test_user, post_id = post.id, content="Test2 content")
        Comment.objects.create(username = test_user, post_id = post.id, content="Test3 content")

    def test_comment_content(self):
        test1 = Comment.objects.get(content="Test1 content")
        test2 = Comment.objects.get(content="Test2 content")
        test3 = Comment.objects.get(content="Test3 content")
        self.assertEqual(test1.content, 'Test1 content')
        self.assertEqual(test2.content, 'Test2 content')
        self.assertEqual(test3.content, 'Test3 content')