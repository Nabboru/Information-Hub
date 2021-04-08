from django.test import TestCase
from accounts.models import User
from news.models import News
from datetime import datetime
import pytz

class NewsTestCaseModel(TestCase):
    def setUp(self):
        user_professional = User.objects.create_user(
            'professional',
            email = 'promail@gmail.com',
            password = 'test123',
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


    # Testing the news model
    def test_news_exists(self):
        news_count = News.objects.all().count()
        self.assertEqual(news_count, 1)
        self.assertNotEqual(news_count, 0)

