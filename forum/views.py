from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from accounts.decorators import professional_required, patient_required
from django.utils.decorators import method_decorator
from .models import Comment, ForumPost, AnnouncementPost
from .forms import CommentForm, ForumPostForm
#from .models import User

def forum(request):
    return render(request, 'forum.html', {})

""" Putting the decorator on like will ask the method for an additional request which is not needed
    since it is linked to the detail page.
    method for liking posts """
def LikeView(request, pk):
    post = get_object_or_404(ForumPost, id = request.POST.get('post_id'))
    #post = ForumPost.objects.get(id=request.user.id)
    liked = False
    if post.likes.filter(id = request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    
    return HttpResponseRedirect(reverse('post-details', args = [str(pk)]))

#method for reporting posts
def ReportView(request, pk):
    post = get_object_or_404(ForumPost, id = request.POST.get('post_id'))
    reported = False
    if post.reports.filter(id = request.user.id).exists():
        post.reports.remove(request.user)
        reported = False
    else:
        post.reports.add(request.user)
        reported = True
    
    return HttpResponseRedirect(reverse('post-details', args = [str(pk)]))

#to show all forum posts
@method_decorator(login_required(login_url='/'), name='dispatch')
class PostListView(ListView):
    model = ForumPost
    template_name = 'forum_posts.html'
    context_object_name = 'posts'
    ordering = ['-creation_date']      
    paginate_by = 10
   
    
#to show details of a post
class PostDetailView(DetailView):
    model = ForumPost
    template_name = 'post_details.html'

    
    allow_empty = False # Causes 404 to be raised if queryset is empty 
    def get(self, request, *args, **kwargs):
        try:
            return super(PostDetailView, self).get(request, *args, **kwargs)
        except Http404:
            return HttpResponseRedirect("/forum_posts/")

    #reflects the preference status of a user
    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
       
        details = get_object_or_404(ForumPost, id=self.kwargs['pk'])
        total_likes = details.total_likes()
        total_reports = details.total_reports()

       #This implements the like/unlike button on a post
        liked = False 
        if details.likes.filter(id = self.request.user.id).exists():
            liked = True
 
       #This implements the report functionality on a post
        reported = False
        if details.reports.filter(id = self.request.user.id).exists():
           reported = True

       #If the reports reach a certain number, the post gets deleted
        if total_reports == 5:
            ForumPost.objects.filter(id = details.id).delete()
  
          
        context ["total_likes"] = total_likes
        context ["liked"] = liked
        context ["total_reports"] = total_reports
        context ["reported"] = reported
        
        return context
    
    #gets the id of the currently active user
    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)


# creating posts, upon clicking the create button, 
# user will be redirected to the post creation page
@method_decorator(login_required(login_url='/'), name='dispatch')
class PostCreateView(CreateView):
    model = ForumPost
    template_name = 'create_post.html'
    form_class = ForumPostForm

    #gets the id of the currently active user
    def form_valid(self, form):
        form.instance.username = self.request.user
        try:
            return super().form_valid(form)
        except:
            return HttpResponse("ERROR: A post with this subject already exists!")

@method_decorator(login_required(login_url='/'), name='dispatch')
class PostUpdateView(UpdateView):
    model = ForumPost
    template_name = 'edit_post.html'
    fields = ['subject', 'content']

    def get_success_url(self):
        return reverse_lazy('post-details', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)

@method_decorator(login_required(login_url='/'), name='dispatch')
class PostDeleteView(DeleteView):
    model = ForumPost
    success_url = reverse_lazy('forum-posts')
    template_name = 'post_confirm_delete.html'

@method_decorator(login_required(login_url='/'), name='dispatch')
class MyPostListView(ListView):
    model = ForumPost
    template_name = 'my_posts.html'
    context_object_name = 'posts'
    ordering = ['-creation_date']

@method_decorator(login_required(login_url='/'), name='dispatch')
class CommentListView(ListView):
    model = Comment
    template_name = 'post-details.html'
    context_object_name = 'comments'

@method_decorator(login_required(login_url='/'), name='dispatch')
class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'add_comment.html'
    
    def get_success_url(self):
        return reverse_lazy('post-details', kwargs={'pk': self.kwargs['pk']})


    #gets the id of the post where the comment is getting added and that of the active user
    def form_valid(self, form):
        #form.instance.comment = Comment.objects.get(id=self.kwargs.get("id"))
        form.instance.post = ForumPost.objects.get(pk=self.kwargs.get("pk"))
        form.instance.username = self.request.user
        return super().form_valid(form)
@method_decorator(login_required(login_url='/'), name='dispatch')
class CommentUpdateView(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'edit_comment.html'
    
    def get_success_url(self):
        return reverse_lazy('post-details', kwargs={'pk': self.get_object().post.pk})


    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)

@method_decorator(login_required(login_url='/'), name='dispatch')
class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'comment_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('post-details', kwargs={'pk': self.get_object().post.pk})

    
#the methods below all belong to the CRUD functionality of the announcement section of the forum.
class AnnPostListView(ListView):
    model = AnnouncementPost
    template_name = 'announcements.html'
    context_object_name = 'announcements'
    ordering = ['-creation_date']
    paginate_by = 5

class AnnPostDetailView(DetailView):
    model = AnnouncementPost
    template_name = 'ann_post_details.html'

