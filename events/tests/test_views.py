from django.test import TestCase
from django.test.client import Client
from accounts.models import User
from events.models import Event
from datetime import datetime
from django.conf import settings
from django.urls import reverse
import pytz


class EventTestCaseNoLogin(TestCase):
    def setUp(self):
        self.client = Client()

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

        self.data = {
            'subject' : "Some random subject", 
            'content' : "This is a description of the content",
            'author' : user_professional,
            'start_time' : "2021-03-30T15:30" ,
            'end_time' : "2021-03-30T17:30" ,
            'url': "https://www.geeksforgeeks.org/django-modelform-create-form-from-models/" ,
            'location': "Strand"
        }

    # Test viewing all events without login
    def test_events_view_without_login(self):
        response = self.client.get(reverse('events'), follow=True)
        status_code = response.status_code
        redirect_path = response.request.get("PATH_INFO")

        self.assertNotEqual(redirect_path, reverse('events'))
        self.assertEqual(redirect_path, settings.LOGIN_URL)
        self.assertEqual(status_code, 200)

    # Test viewing the event's details without login
    def test_event_details_without_login(self):
        event_t = Event.objects.get(pk=1)
    
        response = self.client.get(reverse('event_detail', args=[event_t.pk]), follow=True)
        status_code = response.status_code
        redirect_path = response.request.get("PATH_INFO")

        self.assertNotEqual(redirect_path, reverse('event_detail', args=[event_t.pk]))
        self.assertEqual(redirect_path, settings.LOGIN_URL)
        self.assertEqual(status_code, 200)


    # Test creation of events without login
    def test_event_creation_without_login(self):
        response = self.client.post(reverse('event_create'), self.data, follow=True)
        status_code = response.status_code
        redirect_path = response.request.get("PATH_INFO")

        self.assertNotEqual(redirect_path, "event/1/")
        self.assertEqual(redirect_path, settings.LOGIN_URL)
        self.assertEqual(status_code, 200)

    # Test update of events without login
    def test_update_without_login(self):
        event_t = Event.objects.get(pk=1)
        
        response = self.client.post(
            reverse('event_update', args=[event_t.pk]), 
            self.data, 
            follow=True
        )
        
        redirect_path = response.request.get("PATH_INFO")
        self.assertEqual(redirect_path, reverse('login'))

    # Test deletion of events without login
    def test_delete_without_login(self):
        event_t = Event.objects.get(pk=1)
        
        response = self.client.post(reverse('event_delete', args=[event_t.pk]), follow=True)
        
        redirect_path = response.request.get("PATH_INFO")
        self.assertEqual(redirect_path, reverse('login'))

    # Test the booking of an event without login
    def test_book_event_without_login(self):
        event_t = Event.objects.get(pk=1)
        response = self.client.get(reverse('event_book', args=[event_t.pk]))
        self.assertEqual(response.url, '/login/?next=/event/1/book')

    # Test the unbooking of an event without login
    def test_unbook_event_without_login(self):
        event_t = Event.objects.get(pk=1)
        response = self.client.get(reverse('event_unbook', args=[event_t.pk]))
        self.assertEqual(response.url, '/login/?next=/event/1/unbook')


class EventTestCasePatientLogin(TestCase):
    def setUp(self):
        self.client = Client()

        user_patient = User.objects.create_user(
            'patient', 
            email = 'patient@gmail.com', 
            password = 'patient123', 
            first_name = 'Patient', 
            last_name = 'Test', 
            is_patient=True
        )
        user_patient.save()

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

        self.data = {
            'subject' : "Some random subject", 
            'content' : "This is a description of the content",
            'author' : user_professional,
            'start_time' : "2021-03-30T15:30" ,
            'end_time' : "2021-03-30T17:30" ,
            'url': "https://www.geeksforgeeks.org/django-modelform-create-form-from-models/" ,
            'location': "Strand"
        }

    # Test viewing all events with patient login
    def test_events_view_with_patient_login(self):
        self.client.login(username='patient@gmail.com', password='patient123')

        response = self.client.get(reverse('events'), follow=True)
        status_code = response.status_code
        redirect_path = response.request.get("PATH_INFO")

        self.assertEqual(redirect_path, reverse('events'))
        self.assertEqual(status_code, 200)

    # Test viewing the event's details with patient login
    def test_event_details_with_patient_login(self):
        event_t = Event.objects.get(pk=1)

        self.client.login(username='patient@gmail.com', password='patient123')
    
        response = self.client.get(reverse('event_detail', args=[event_t.pk]), follow=True)
        status_code = response.status_code
        redirect_path = response.request.get("PATH_INFO")

        self.assertEqual(redirect_path, reverse('event_detail', args=[event_t.pk]))
        self.assertEqual(status_code, 200)

    # Testing event creation with patient login
    def test_event_creation_with_unauthorised_login(self):
        self.client.login(username='patient@gmail.com', password='patient123')
        response = self.client.post("/event/new", self.data, follow=True)
        redirect_path = response.request.get("PATH_INFO")
        self.assertNotEqual(redirect_path, "/event/2/")
        self.assertEqual(redirect_path, "/login/")

    # Test update of events with patient login
    def test_update_with_unauthorised_login(self):
        event_t = Event.objects.get(pk=1)
        
        self.client.login(username='patient@gmail.com', password='patient123')
        response = self.client.post(
            reverse('event_update', args=[event_t.pk]), 
            self.data, 
            follow=True
        )
        
        redirect_path = response.request.get("PATH_INFO")
        self.assertEqual(redirect_path, reverse('login'))
        event_t.refresh_from_db()
        self.assertNotEqual(event_t.content, "This is updated")
        self.assertEqual(event_t.content, "This is a description of the content")
        
    # Test deletion of events with patient login
    def test_delete_with_unauthorised_login(self):
        event_t = Event.objects.get(pk=1)
        
        self.client.login(username='patient@gmail.com', password='patient123')
        response = self.client.post(reverse('event_delete', args=[event_t.pk]), follow=True)
        
        redirect_path = response.request.get("PATH_INFO")
        self.assertEqual(redirect_path, reverse('login'))

    # Test the booking of an event with patient login
    def test_book_event_with_patient_login(self):
        event_t = Event.objects.get(pk=1)
        
        self.client.login(username='patient@gmail.com', password='patient123')
        response = self.client.get(reverse('event_book', args=[event_t.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'event_book_confirm.html')
    
    # Test the unbooking of an event with patient login
    def test_unbook_event_with_patient_login(self):
        event_t = Event.objects.get(pk=1)
        
        self.client.login(username='patient@gmail.com', password='patient123')
        response = self.client.get(reverse('event_unbook', args=[event_t.pk]))

        self.assertEqual(response.status_code, 302)


class EventTestCaseProfessionalLogin(TestCase):
    def setUp(self):
        self.client = Client()

        user_professional = User.objects.create_user(
            'professional', 
            email = 'professional@gmail.com', 
            password = 'test123', 
            first_name = 'Professional', 
            last_name = 'Test', 
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
        
        event_a = Event(
            subject = "Some random subject", 
            content = "This is a description of the content",
            author = user_professional,
            start_time = datetime(2021, 3, 14, 18, 12, 12, 127325, tzinfo=pytz.UTC),
            end_time = datetime(2021, 3, 14, 20, 12, 12, 127325, tzinfo=pytz.UTC)
        )
        event_a.save()

        self.data = {
            'subject' : "Some random subject", 
            'content' : "This is a description of the content",
            'author' : user_professional,
            'start_time' : "2021-03-30T15:30" ,
            'end_time' : "2021-03-30T17:30" ,
            'url': "https://www.geeksforgeeks.org/django-modelform-create-form-from-models/" ,
            'location': "Strand"
        }

        self.changed_data = {
            'subject' : "Some random subject", 
            'content' : "This is updated",
            'author' : user_professional,
            'start_time' : "2021-03-30T15:30" ,
            'end_time' : "2021-03-30T17:30" ,
            'url': "https://www.geeksforgeeks.org/django-modelform-create-form-from-models/" ,
            'location': "Strand"
        }

    # Test viewing all events with professional login
    def test_events_view_with_patient_login(self):
        self.client.login(username='professional@gmail.com', password='test123')

        response = self.client.get(reverse('events'), follow=True)
        status_code = response.status_code
        redirect_path = response.request.get("PATH_INFO")

        self.assertEqual(redirect_path, reverse('events'))
        self.assertEqual(status_code, 200)

    # Test viewing the event's details with professional login
    def test_event_details_with_patient_login(self):
        event_t = Event.objects.get(pk=1)

        self.client.login(username='professional@gmail.com', password='test123')
    
        response = self.client.get(reverse('event_detail', args=[event_t.pk]), follow=True)
        status_code = response.status_code
        redirect_path = response.request.get("PATH_INFO")

        self.assertEqual(redirect_path, reverse('event_detail', args=[event_t.pk]))
        self.assertEqual(status_code, 200)

    # Testing event creation with professional login
    def test_event_creation_with_authorised_login(self):        
        self.client.login(username='professional@gmail.com', password='test123')
        response = self.client.post("/event/new", self.data, follow=True)
        redirect_path = response.request.get("PATH_INFO")
        self.assertEqual(redirect_path, "/event/2/")
        self.assertEqual(response.status_code, 200)

    # Test update of events with professional login
    def test_update_with_authorised_login(self):
        event_t = Event.objects.get(pk=1)

        self.client.login(username='professional@gmail.com', password='test123')
        response = self.client.post(
            reverse('event_update', args=[event_t.pk]), 
            self.changed_data, 
            follow=True
        )
        
        redirect_path = response.request.get("PATH_INFO")
        self.assertEqual(redirect_path, reverse('event_detail', args=[event_t.pk]))
        event_t.refresh_from_db()
        self.assertEqual(event_t.content, "This is updated")
        
    # Test update of events with different author than the one which created the event
    def test_update_with_different_author(self):
        event_t = Event.objects.get(pk=1)
       
        self.client.login(username='professional2@gmail.com', password='test123')
        response = self.client.post(
            reverse('event_update', args=[event_t.pk]), 
            self.changed_data, 
            follow=True
        )
        
        self.assertEqual(response.status_code, 403)

    # Test deletion of events with professional login
    def test_delete_with_authorised_login(self):
        event_t = Event.objects.get(pk=1)
        
        self.client.login(username='professional@gmail.com', password='test123')
        response = self.client.post(reverse('event_delete', args=[event_t.pk]), follow=True)
        
        redirect_path = response.request.get("PATH_INFO")
        self.assertEqual(redirect_path, reverse('home'))

        event_count = Event.objects.all().count()
        self.assertEqual(event_count, 0)

    # Test deletion of events with different author than the one which created the event
    def test_delete_with_different_author(self):
        user_t = User.objects.get(email="professional@gmail.com")
        event_t = Event.objects.get(pk=1)

        self.client.login(username='professional2@gmail.com', password='test123')
        response = self.client.post(reverse('event_delete', args=[event_t.pk]), follow=True)
        
        self.assertEqual(response.status_code, 403)
        event_count = Event.objects.all().count()
        self.assertEqual(event_count, 1) 

    # Test the booking of an event with professional login
    def test_book_event_with_prof_login(self):
        event_t = Event.objects.get(pk=1)
        
        self.client.login(username='professional2@gmail.com', password='test123')
        response = self.client.get(reverse('event_book', args=[event_t.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'event_book_confirm.html')
    
    # Test the unbooking of an event with professional login
    def test_unbook_event_with_prof_login(self):
        event_t = Event.objects.get(pk=1)
        
        self.client.login(username='professional2@gmail.com', password='test123')
        response = self.client.get(reverse('event_unbook', args=[event_t.pk]))

        self.assertEqual(response.status_code, 302)