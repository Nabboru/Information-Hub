from django.db import models

class FAQPost(models.Model):
    question = models.TextField()
    answer = models.TextField()
    last_modified = models.DateTimeField(auto_now=True)
