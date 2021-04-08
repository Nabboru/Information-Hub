from django.test import TestCase
from django.test.client import Client
from accounts.models import User
from news.models import News
from datetime import datetime
from django.conf import settings
from django.urls import reverse
import pytz


class NewsTestCaseNoLogin(TestCase):
    def setUp(self):

        user_professional = User.objects.create_user(
            'professional',
            email = 'promail@gmail.com',
            password = '123test',
            first_name = 'Professional',
            last_name = 'Testing',
            is_professional=True
        )
        user_professional.save()

        news_x = News(
            title = "A Sample Article Title",
            content = "This is a description of the content",
            creation_date = datetime(2021, 3, 14, 18, 12, 12, 127325, tzinfo=pytz.UTC),
            author = user_professional
        )
        news_x.save()

        self.data = {
            'subject' : "A Sample Article Title",
            'content' : "This is a description of the content",
            'creation_date' : "2021-03-30T15:30" ,
            'author' : user_professional,
        }

    # Testing the creation of news without login
    def test_news_creation_without_login(self):
        response = self.client.post(reverse('news_create'), self.data, follow=True)
        status_code = response.status_code
        redirect_path = response.request.get("PATH_INFO")

        self.assertNotEqual(redirect_path, "news/1/")
        self.assertEqual(redirect_path, settings.LOGIN_URL)
        self.assertEqual(status_code, 200)

    # Testing the update of news without login
    def test_update_without_login(self):
        news_y = News.objects.get(pk=1)

        response = self.client.post(
            reverse('news_update', args=[news_y.pk]),
            self.data,
            follow=True
        )

        redirect_path = response.request.get("PATH_INFO")
        self.assertEqual(redirect_path, reverse('login'))

    # Testing the deletion of news without login
    def test_delete_without_login(self):
        news_y = News.objects.get(pk=1)

        response = self.client.post(reverse('news_delete', args=[news_y.pk]), follow=True)

        redirect_path = response.request.get("PATH_INFO")
        self.assertEqual(redirect_path, reverse('login'))


class NewsTestCasePatientLogin(TestCase):
    def setUp(self):

        user_patient = User.objects.create_user(
            'patient',
            email = 'patientmail@gmail.com',
            password = '123patient',
            first_name = 'Patient',
            last_name = 'Testing',
            is_patient=True
        )
        user_patient.save()

        user_professional = User.objects.create_user(
            'professional',
            email = 'promail@gmail.com',
            password = '123pro',
            first_name = 'Professional',
            last_name = 'Testing',
            is_professional=True
        )
        user_professional.save()

        news_x = News(
            title = "A Sample Article Title",
            content = "This is a description of the content",
            author = user_professional,
            creation_date = datetime(2021, 3, 14, 18, 12, 12, 127325, tzinfo=pytz.UTC)
        )
        news_x.save()

        self.data = {
            'title' : "A Sample Article Title",
            'content' : "This is a description of the content",
            'author' : user_professional,
            'creation_date' : "2021-03-30T15:30" ,
        }

    # Testing news creation with patient login
    def test_news_creation_with_unauthorised_login(self):
        self.client.login(username='patient@gmail.com', password='123patient')
        response = self.client.post("/news/new", self.data, follow=True)
        redirect_path = response.request.get("PATH_INFO")
        self.assertNotEqual(redirect_path, "/news/2/")
        self.assertEqual(redirect_path, "/login/")

    # Testing the update of news with patient login
    def test_update_with_unauthorised_login(self):
        news_y = News.objects.get(pk=1)

        self.client.login(username='patient@gmail.com', password='123patient')
        response = self.client.post(
            reverse('news_update', args=[news_y.pk]),
            self.data,
            follow=True
        )

        redirect_path = response.request.get("PATH_INFO")
        self.assertEqual(redirect_path, reverse('login'))
        news_y.refresh_from_db()
        self.assertNotEqual(news_y.content, "This is an updated version.")
        self.assertEqual(news_y.content, "This is a description of the content")

    # Testing the deletion of news with patient login
    def test_delete_with_unauthorised_login(self):
        news_y = News.objects.get(pk=1)

        self.client.login(username='patientmail@gmail.com', password='123patient')
        response = self.client.post(reverse('news_delete', args=[news_y.pk]), follow=True)

        redirect_path = response.request.get("PATH_INFO")
        self.assertEqual(redirect_path, reverse('login'))


class NewsTestCaseProfessionalLogin(TestCase):
    def setUp(self):

        user_professional = User.objects.create_user(
            'professional',
            email = 'professional@gmail.com',
            password = '123test',
            first_name = 'Professional',
            last_name = 'Testing',
            is_professional=True
        )
        user_professional.save()

        user_professional2 = User.objects.create_user(
            'professional2',
            email = 'professional2@gmail.com',
            password = 'test123',
            first_name = 'Professional',
            last_name = 'Test',
            is_professional = True
        )
        user_professional2.save()

        news_x = News(
            title = "A Sample Article Title",
            content = "This is a description of the content",
            author = user_professional,
            creation_date = datetime(2021, 3, 14, 18, 12, 12, 127325, tzinfo=pytz.UTC)
        )
        news_x.save()

        self.data = {
            'title' : "A Sample Article Title",
            'content' : "This is a description of the content",
            'author' : user_professional,
            'creation_date' : "2021-03-30T15:30" ,
        }

        self.changed_data = {
            'title' : "A Sample Article Title",
            'content' : "This is updated",
            'author' : user_professional,
            'creation_date' : "2021-03-30T15:30" ,
        }

    # Testing the news creation with professional login
    def test_news_creation_with_authorised_login(self):
        self.client.login(username='professional@gmail.com', password='123test')
        response = self.client.post("/news/new", self.data, follow=True)
        redirect_path = response.request.get("PATH_INFO")
        self.assertEqual(redirect_path, "/news/")
        self.assertEqual(response.status_code, 200)

    # Testing the update of news with professional login
    def test_update_with_authorised_login(self):
        news_y = News.objects.get(pk=1)

        self.client.login(username='professional@gmail.com', password='123test')
        response = self.client.post(
            reverse('news_update', args=[news_y.pk]),
            self.changed_data,
            follow=True
        )

        redirect_path = response.request.get("PATH_INFO")
        self.assertEqual(redirect_path, reverse('news_detail', args=[news_y.pk]))
        news_y.refresh_from_db()
        self.assertEqual(news_y.content, "This is updated")

    # Testing the update of news with an author different from the one who published the article
    def test_update_with_different_author(self):
        news_y = News.objects.get(pk=1)

        self.client.login(username='professional2@gmail.com', password='test123')
        response = self.client.post(
            reverse('news_update', args=[news_y.pk]),
            self.changed_data,
            follow=True
        )

        self.assertEqual(response.status_code, 403)

    # Testing the deletion of news with professional login
    def test_delete_with_authorised_login(self):
        news_y = News.objects.get(pk=1)

        self.client.login(username='professional@gmail.com', password='123test')
        response = self.client.post(reverse('news_delete', args=[news_y.pk]), follow=True)

        redirect_path = response.request.get("PATH_INFO")
        self.assertEqual(redirect_path, reverse('news'))

        news_count = News.objects.all().count()
        self.assertEqual(news_count, 0)

    # Testing the deletion of news with an author different from the one who published the article
    def test_delete_with_different_author(self):
        user_y = User.objects.get(email="professional2@gmail.com")
        news_y = News.objects.get(pk=1)

        self.client.login(username='professional2@gmail.com', password='test123')
        response = self.client.post(reverse('news_delete', args=[news_y.pk]), follow=True)

        self.assertEqual(response.status_code, 403)
        news_count = News.objects.all().count()
        self.assertEqual(news_count, 1)
