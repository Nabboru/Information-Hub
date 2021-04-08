from django.db import models
from django.urls import reverse

from ckeditor_uploader.fields import RichTextUploadingField

class News(models.Model):
    # Contains title,content, creation_date, last_modified, url and author
    title = models.CharField(max_length = 200)
    content = RichTextUploadingField()
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey('accounts.User', null=True, on_delete= models.SET_NULL)

# Represents the news through its subject field
def __str__(self):
  return self.subject

# Returns to news summary after create or update
def get_absolute_url(self):
    return reverse('news_detail', kwargs={'pk' : self.pk})
