from django.test import TestCase
from events.models import Event
from accounts.models import User
from django.urls import reverse
from datetime import datetime
from accounts.models import User
import pytz
from django.test import Client

# Calendar tests.
class CalendarEventTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_superuser(username= 'user', email= 'user@email.com' , password = '123456')
        user.save()
        # make a client
        self.client = Client()

    def test_calendar_response(self):
        # Issue a GET request.
        response = self.client.get('/calendar/')

        # Check that the response is 302 Redirect when not logged in.
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/calendar/')

        # Log in and issue another GET request.
        self.client.post('/login/', {'username': 'user@email.com', 'password': '123456'})
        response = self.client.get('/calendar/')

        # Check that the response is 200 OK when logged in.
        self.assertEqual(response.status_code, 200)

       