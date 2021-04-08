from django.conf.urls import url
from django.urls import path, include
from help_support import views

app_name = 'help_support'
urlpatterns = [
    path('help_support/', views.help_support, name='help'),
]
