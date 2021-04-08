from django.db import models

class HelpSupportPost(models.Model):
    name = models.TextField()
    details = models.TextField()
    contact = models.TextField()
    last_modified = models.DateTimeField(auto_now=True)
