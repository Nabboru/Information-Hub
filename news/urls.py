from django.urls import path
from .views import (
    NewsListView,
    NewsDetailView,
    NewsCreateView,
    NewsDeleteView,
    NewsUpdateView
)

urlpatterns = [
    path('', NewsListView.as_view(), name='news'),
    path('<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
    path('new', NewsCreateView.as_view(), name='news_create'),
    path('<int:pk>/delete', NewsDeleteView.as_view(), name='news_delete'),
    path('<int:pk>/update', NewsUpdateView.as_view(), name='news_update'),
]
