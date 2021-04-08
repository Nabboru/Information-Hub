from django.contrib import admin
from .models import ForumPost
from .models import AnnouncementPost
from .models import Comment

admin.site.register(ForumPost)
admin.site.register(AnnouncementPost)
admin.site.register(Comment)


