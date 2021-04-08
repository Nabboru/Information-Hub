from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField

class Event(models.Model):
  # Subject, Content, Author of Event, Creation Date, Start Date, End Date, Online Meeting Link, Location of Event
  subject = models.CharField(max_length = 30)
  content = RichTextUploadingField()
  author = models.ForeignKey('accounts.User',  null=True, on_delete= models.SET_NULL, related_name='author')
  participants = models.ManyToManyField('accounts.User', related_name='participants')
  creation_date = models.DateField(auto_now_add=True)
  start_time = models.DateTimeField()
  end_time = models.DateTimeField()
  url = models.URLField(null=True, blank=True)
  location = models.CharField(max_length = 50,  null=True, blank=True)

  # Represent the event object through its subject field
  def __str__(self):
    return self.subject

  def get_absolute_url(self):
    return reverse('event_detail', kwargs={'pk' : self.pk})

  # Event link for the calendar
  @property
  def get_html_url(self):
    url = reverse('event_detail', args=(self.id,))
    return f'<a href="{url}"> {self.start_time.time().hour}:{self.start_time.time().minute} - {self.end_time.time().hour}:{self.end_time.time().minute}</a>'
