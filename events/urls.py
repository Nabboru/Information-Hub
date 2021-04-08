from django.urls import path
from . import views
from .views import (
    EventListView, 
    EventDetailView,
    EventCreateView,
    EventUpdateView,
    EventDeleteView,
    #EventBookView
)

urlpatterns = [
    path('events/', EventListView.as_view(), name='events'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('event/new', EventCreateView.as_view(), name='event_create'),
    path('event/<int:pk>/update', EventUpdateView.as_view(), name='event_update'),
    path('event/<int:pk>/delete', EventDeleteView.as_view(), name='event_delete'),
    path('event/<int:pk>/book', views.event_book, name='event_book'),
    path('event/<int:pk>/unbook', views.event_unbook, name='event_unbook'),
]