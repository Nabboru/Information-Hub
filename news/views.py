from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView
)
# Create the views here.
from django.contrib.auth.decorators import login_required
from accounts.decorators import professional_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy, reverse
from .models import News
from .forms import NewsForm

# Viewing all news as a logged-in user
class NewsListView(ListView):
    model = News
    template_name = 'all_news.html'
    context_object_name = 'news'
    ordering = ['-creation_date']
    paginate_by = 5

# Viewing news summary as a logged-in user
class NewsDetailView(DetailView):
    model = News
    template_name = "news_detail.html"

# Creating the news only when logged in as a professional
@method_decorator(professional_required, name='dispatch')
class NewsCreateView(CreateView):
    model = News
    template_name = "news_form.html"
    form_class = NewsForm
    success_url = reverse_lazy('news')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# Deleting a news article only when logged in as a professional
@method_decorator(professional_required, name='dispatch')
class NewsDeleteView(UserPassesTestMixin, DeleteView):
    model = News
    template_name = "news_delete.html"

    # Redirect back to home page if deletion is successful
    success_url = reverse_lazy('news')

    # Checking if the authour making the delete request is the same as the one who created the news article
    def test_func(self):
        news = self.get_object()
        if self.request.user == news.author:
            return True
        return False

# Updating an article only when logged in as a professional
@method_decorator(professional_required, name='dispatch')
class NewsUpdateView(UserPassesTestMixin, UpdateView):
    model = News
    template_name = "news_form.html"
    form_class = NewsForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # Checking if the authour making the update request is the same as the one who created the news article
    def test_func(self):
        post = self.get_object()
        print(post.author)
        if self.request.user == post.author:
            return True
        return False
    
    def get_success_url(self):
        return reverse_lazy('news_detail', kwargs={'pk': self.kwargs['pk']})
