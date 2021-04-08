from django.test import TestCase
from accounts.models import User
from events.models import Event
from datetime import datetime
from django.urls import reverse
import pytz


class EventTestCaseModel(TestCase):
    def setUp(self):
        user_professional = User.objects.create_user(
            'professional', 
            email = 'professional@gmail.com', 
            password = 'test123', 
            first_name = 'Professional', 
            last_name = 'Test', 
            is_professional=True
        )
        user_professional.save()
        
        event_a = Event(
            subject = "Some random subject", 
            content = "This is a description of the content",
            author = user_professional,
            start_time = datetime(2021, 3, 14, 18, 12, 12, 127325, tzinfo=pytz.UTC),
            end_time = datetime(2021, 3, 14, 20, 12, 12, 127325, tzinfo=pytz.UTC)
        )
        event_a.save()
    

    # Test event model
    def test_event_exists(self):
        event_count = Event.objects.all().count()
        self.assertEqual(event_count, 1)
        self.assertNotEqual(event_count, 0)

    #Test link for calendar events
    def test_get_events_html(self):
        event = Event.objects.get(subject="Some random subject")
        url = reverse('event_detail', args=(event.id,))
        self.assertEqual(event.get_html_url, f'<a href="{url}"> 18:12 - 20:12</a>')

    

    # Test booking for an event
    def test_event_book(self):
        event = Event.objects.get(id=1)
        user = User.objects.get(id=1)
        event.value = event.participants.add(user)
        event.save()
        event_count = Event.objects.all().count()
        self.assertEqual(event_count, 1)
        self.assertNotEqual(event_count, 0)
        self.assertEqual(event.participants, Event.objects.get(id=1).participants)
        self.assertEqual(event.subject, Event.objects.get(id=1).subject)

    # Test unbooking for an event
    def test_event_unbook(self):
        event = Event.objects.get(id=1)
        user = User.objects.get(id=1)
        event.value = event.participants.add(user)
        event.save()
        event.value = event.participants.remove(user)
        event.save()
        event_count = Event.objects.all().count()
        participants_count = Event.objects.get(id=1).participants.count()
        self.assertEqual(event_count, 1)
        self.assertNotEqual(event_count, 0)
        self.assertEqual(participants_count, 0)
        self.assertEqual(event.participants, Event.objects.get(id=1).participants)
        self.assertEqual(event.subject, Event.objects.get(id=1).subject)