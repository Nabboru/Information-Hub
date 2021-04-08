from django.test.client import Client
from accounts.models import User
from forum.models import ForumPost, Comment, AnnouncementPost
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse_lazy, reverse


class PostCreateViewTest(TestCase):
    def setUp(self):
        user_email = 'testing@email.com'
        test_user = User.objects.create_user(username= 'test', email= user_email, password = 'testing@123', is_patient = True)
        test_user.save()
        self.client.login(username=user_email, password='testing@123')

   #Creates a post and asserts that it's in the database
    def test_create_post(self):
        test_u = User.objects.get(email='testing@email.com')
        response = self.client.get(reverse('create-post'))
        response = self.client.post(reverse('create-post'), {'username' : test_u, 'subject' : "Super Important Test", 'content' : "This is really important.", 'for_patient' : True, 'creation_date' : timezone.now()})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ForumPost.objects.get(pk=1).subject, "Super Important Test")
        
class PostDetailViewTest(TestCase):
    def setUp(self):
        user_email = 'testing@email.com'
        test_user = User.objects.create_user(username= 'test', email= user_email, password = 'testing@123')
        test_user.save()
        fpost = ForumPost.objects.create(username = test_user, subject = "Super Important Test", content = "This is really important.", creation_date = timezone.now(), for_patient = True, for_family = False)
        self.client.login(username=user_email, password='testing@123')

   #Checks that the detail view is displayed after directly creating a post
    def test_detail_post(self):
        fpost_t = ForumPost.objects.get(pk=1)
        response = self.client.get(reverse('post-details', args=[fpost_t.pk]))
        self.assertEqual(response.status_code, 200)

class PostUpdateViewTest(TestCase):
    def setUp(self):
        user_email = 'testing@email.com'
        test_user = User.objects.create_user(username= 'test', email= user_email, password = 'testing@123')
        test_user.save()
        fpost = ForumPost.objects.create(username = test_user, subject = "Super Important Test", content = "This is really important.", creation_date = timezone.now(), for_patient = True, for_family = False)
        fpost.save()
        self.client.login(username=user_email, password='testing@123')

   #Checks that post has been successfully upedated and stored in the database
    def test_update_post(self):
        fpost_t = ForumPost.objects.get(pk=1)
        response = self.client.post(reverse('post-update', args=[1]), 
            {'username': fpost_t.username, 'subject': "The Coolest", 'content': "I am cool",  'for_patient' : 'True', 'for_family' : 'False'},
            follow = True)
        redirect_path = response.request.get("PATH_INFO")
        self.assertEqual(redirect_path, reverse('post-details', args=[fpost_t.pk]))
        fpost_t.refresh_from_db()
        self.assertEqual(fpost_t.content, 'I am cool')


class PostDeleteViewTest(TestCase):
    def setUp(self):
        user_email = 'testing@email.com'
        test_user = User.objects.create_user(username= 'test', email= user_email, password = 'testing@123')
        test_user.save()
        fpost = ForumPost.objects.create(username = test_user, subject = "Super Important Test", content = "This is really important.", creation_date = timezone.now(), for_patient=True, for_family=False)
        self.client.login(username=user_email, password='testing@123')

   #Checks that after the post has been deleted, it redirects to forum_posts
    def test_delete_post(self):
        fpost_t = ForumPost.objects.get(pk=1)
        response = self.client.post(reverse('post-delete', args =[fpost_t.pk]), follow=True)

        redirect_path = response.request.get("PATH_INFO")
        self.assertEqual(redirect_path, reverse('forum-posts'))

        posts_count = ForumPost.objects.all().count()
        self.assertEqual(posts_count, 0)

class CommentCreateViewTest(TestCase):
    def setUp(self):
        user_email = 'testing@email.com'
        test_user = User.objects.create_user(username= 'test', email= user_email, password = 'testing@123', is_professional = True)
        test_user.save()
        fpost = ForumPost.objects.create(username = test_user, subject = "Super Important Test", content = "This is really important.", creation_date = timezone.now(), for_family=True, for_patient=True)
        self.client.login(username=user_email, password='testing@123')

    def test_add_comment(self):
        fpost_t = ForumPost.objects.get(pk=1)
        test_u = User.objects.get(pk=1)
        self.client.post(reverse('add-comment', args=[1]), {'username' : test_u, 'post' : fpost_t.id, 'content' : "This is really important.", 'creation_date' : timezone.now()})
        self.assertEqual(Comment.objects.get(pk=1).content, "This is really important.")

class CommmentDetailViewTest(TestCase):
    def setUp(self):
        user_email = 'testing@email.com'
        test_user = User.objects.create_user(username= 'test', email= user_email, password = 'testing@123')
        test_user.save()
        post = ForumPost.objects.create(username = test_user, subject = "Super Important Test", content = "This is really important.", creation_date = timezone.now())
        comment = Comment.objects.create(username = test_user, content = "Super excited.", creation_date=timezone.now(), post = post)
        self.client.login(username=user_email, password='testing@123')

   #Checks that the detail view is displayed after directly creating a post
    def test_detail_comment(self):
        fpost_t = ForumPost.objects.get(pk=1)
        comment_t = Comment.objects.get(pk=1)
        response = self.client.get(reverse('post-details', args=[comment_t.pk]))
        self.assertEqual(response.status_code, 200)

class CommentUpdateViewTest(TestCase):
    def setUp(self):
        user_email = 'testing@email.com'
        test_user = User.objects.create_user(username= 'test', email= user_email, password = 'testing@123', is_professional = True)
        test_user.save()
        fpost = ForumPost.objects.create(username = test_user, subject = "Super Important Test", content = "This is really important.", creation_date = timezone.now(), for_patient=True, for_family=True)
        comment = Comment.objects.create(username = test_user, content = "Super excited.", creation_date=timezone.now(), post = fpost)
        self.client.login(username=user_email, password='testing@123')

   #Checks that post has been successfully upedated and stored in the database
    def test_update_comment(self):
        fpost_t = ForumPost.objects.get(pk=1)
        comment_t = Comment.objects.get(pk=1)
        response = self.client.post(reverse('edit-comment', args=[comment_t.pk]), {'username': comment_t.username, 'content' : 'I am cool.'})
        self.assertRedirects(response, reverse('post-details', args =[fpost_t.pk]), status_code=302)
        comment_t.refresh_from_db()
        self.assertEqual(comment_t.content, 'I am cool.')

class CommentDeleteViewTest(TestCase):
    def setUp(self):
        user_email = 'testing@email.com'
        test_user = User.objects.create_user(username= 'test', email= user_email, password = 'testing@123', is_professional = True)
        test_user.save()
        fpost = ForumPost.objects.create(username = test_user, subject = "Super Important Test", content = "This is really important.", creation_date = timezone.now(), for_family=True, for_patient=True)
        comment = Comment.objects.create(username = test_user, content = "Super excited.", creation_date=timezone.now(), post = fpost)
        self.client.login(username=user_email, password='testing@123')

   #Checks that after the comment has been deleted, it redirects to post-details
    def test_delete_comment(self):
        fpost_t = ForumPost.objects.get(pk=1)
        comment_t = Comment.objects.get(pk=1)
        response = self.client.post(reverse('delete-comment', args=[comment_t.pk]))
        self.assertRedirects(response, reverse('post-details', args=[fpost_t.pk]), status_code=302)

class AnnPostDetailViewTest(TestCase):
    def setUp(self):
        user_email = 'testing@email.com'
        test_user = User.objects.create_superuser(username= 'test', email= user_email, password = 'testing@123')
        test_user.save()
        post = AnnouncementPost.objects.create(subject = "Super Important Test", content = "This is really important.", creation_date = timezone.now())
        post.save()
        self.client.login(username=user_email, password='testing@123')

   #Checks that the detail view is displayed after directly creating a post
    def test_detail_post(self):
        post_t = AnnouncementPost.objects.get(pk=1)
        response = self.client.get(reverse('ann-post-details', args=[post_t.pk]))
        self.assertEqual(response.status_code, 200)