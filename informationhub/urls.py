from django.contrib import admin
from django.urls import path, include
from pages import views as pages_views
from faq import views as faq_views
from help_support import views as help_views


urlpatterns = [
    path('', pages_views.home, name='home'),
    path('admin-hub-panel/', admin.site.urls),
    path('about/', pages_views.about, name='about'),
    path('', include('events.urls')),
    path('hub/', include('hub.urls')),
    path('', include('forum.urls')),
    path('news/', include('news.urls')),
    path('', include('accounts.urls')),
    path('', include('calendars.urls', namespace='calendar')),
    path('faq/', faq_views.faq, name='faq'),
    path('help/', help_views.help_support, name='help')
    
]

from django.contrib.auth.decorators import login_required
from ckeditor_uploader.views import upload
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += [
    url(r'^ckeditor/upload/', login_required(upload), name='ckeditor_upload'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
