from django.test import TestCase
from forum.forms import ForumPostForm, CommentForm, AnnouncementForm

class ForumFormTest(TestCase):
    def test_forum_post_form_valid_data(self):
        form = ForumPostForm(data={
            'subject': 'Puppies',
            'content': 'I love them.',
            'for_patient': True,
            'for_family' : False
        })
        self.assertTrue(form.is_valid())

    def test_forum_post_form_no_data(self):
        form = ForumPostForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

class CommentFormTest(TestCase):
    def test_comment_form_valid_data(self):
        form = CommentForm(data={
            'content': 'Me too.'
        })
        self.assertTrue(form.is_valid())

    def test_comment_form_no_data(self):
        form = CommentForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

class AnnouncementFormTest(TestCase):
    def test_announcement_form_valid_data(self):
        form = AnnouncementForm(data={
            'subject': 'Forum guidance',
            'content': 'Rules to follow.'
        })
        self.assertTrue(form.is_valid())

    def test_announcement_form_no_data(self):
        form = AnnouncementForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)