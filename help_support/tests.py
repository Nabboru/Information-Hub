from django.test import TestCase
from .models import HelpSupportPost
from datetime import datetime
from django.test import Client

# The help_support tests.
class HelpSupportPostTestCase(TestCase):
    def setUp(self):
        HelpSupportPost.objects.create(
            name="Adfam", 
            details="Answer test One.", 
            contact="Answer test One.", 
            last_modified=datetime.now())
        HelpSupportPost.objects.create(
            name="Adfam2", 
            details="test One.", 
            contact="test One.", 
            last_modified=datetime.now())
        # make a client
        self.client = Client()

    # Test the help_support post model.
    def test_help_support_fields(self):
        help_support = HelpSupportPost.objects.get(name="Adfam")
        self.assertEqual(help_support.name, "Adfam")
        self.assertEqual(help_support.details, "Answer test One.")
        self.assertEqual(help_support.contact, "Answer test One.")

    def test_help_support_list(self):
        # Issue a GET request.
        response = self.client.get('/help/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the rendered context contains 2 help_support posts.
        self.assertEqual(len(response.context['help_support']), 2)
