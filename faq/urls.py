from django.conf.urls import url
from django.urls import path, include
from faq import views

app_name = 'faq'
urlpatterns = [
    path('faq/', views.faq, name='FAQ'),
]
