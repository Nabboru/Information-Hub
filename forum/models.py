from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField

class ForumPost(models.Model):
    subject = models.CharField(max_length = 300, unique=True)
    content = RichTextUploadingField()
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'forum_posts')
    reports = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name= 'fposts')
    for_patient = models.BooleanField(default=False)
    for_family = models.BooleanField(default=False)


    def total_likes(self):
        return self.likes.all().count()

    def total_reports(self):
        return self.reports.all().count()

    class Meta:
        ordering = ['-creation_date']

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('post-details', kwargs={'pk': self.pk})

class Comment(models.Model):
    content = RichTextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    post = models.ForeignKey(ForumPost, related_name= "comments", on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s' % (self.post.id, self.username)


    def get_absolute_url(self):
        return reverse('post-details', kwargs={'pk': self.pk})


class AnnouncementPost(models.Model):
    subject = models.CharField(max_length= 300, unique=True)
    content = RichTextUploadingField()
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    #username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)

    class Meta:
        ordering = ['-creation_date']

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('ann-post-details', kwargs={'pk': self.pk})
