from django.test import TestCase
from .models import FAQPost
from datetime import datetime
from django.test import Client

# The FAQ tests.
class FAQPostTestCase(TestCase):
    def setUp(self):
        FAQPost.objects.create(
            question="Question test One?", 
            answer="Answer test One.", 
            last_modified=datetime.now())
        FAQPost.objects.create(
            question="Question test Two?", 
            answer="Answer test Two.", 
            last_modified=datetime.now())
        # make a client
        self.client = Client()

    # Test the FAQ post model.
    def test_faq_fields(self):
        faq = FAQPost.objects.get(question="Question test One?")
        self.assertEqual(faq.question, "Question test One?")
        self.assertEqual(faq.answer, "Answer test One.")

    def test_faq_list(self):
        # Issue a GET request.
        response = self.client.get('/faq/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the rendered context contains 2 FAQ posts.
        self.assertEqual(len(response.context['faq']), 2)
