from django.conf.urls import url
from . import views

app_name = 'calendars'
urlpatterns = [
    url(r'^calendar/$', views.CalendarView.as_view(), name='calendar'),
]
