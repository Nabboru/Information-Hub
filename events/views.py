from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)

from django.contrib.auth.decorators import login_required
from accounts.decorators import professional_required, patient_required
from django.utils.decorators import method_decorator
from .models import Event
from .forms import EventForm

# View all events as a logged-in user
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class EventListView(ListView):
    model = Event
    template_name = 'all_events.html'
    context_object_name = 'events'
    ordering = ['-start_time']

# View event details as a logged-in user
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class EventDetailView(DetailView):
    model = Event
    template_name = "event_detail.html"

    def get_context_data(self, **kwargs):
        event = self.get_object()
        context = super().get_context_data(**kwargs)
        context['participants'] = event.participants.all()
        if self.request.user in event.participants.all():
            context['is_user_booked'] = True
        else:
            context['is_user_booked'] = False
        return context

# Create an event only if logged in as a professional
@method_decorator(professional_required, name='dispatch')
class EventCreateView(CreateView):
    model = Event
    template_name = "event_form.html"
    form_class = EventForm

    # Specify the current user as the author of the event
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# Update an event only if logged in as a professional
@method_decorator(professional_required, name='dispatch')
class EventUpdateView(UserPassesTestMixin, UpdateView):
    model = Event
    template_name = "event_form.html"
    form_class = EventForm

    # Specify the current user as the author of the event
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # Check if the authour making the update request is the same as the one who created the event
    def test_func(self):
        event = self.get_object()
        if self.request.user == event.author:
            return True
        return False

# Delete an event only if logged in as a professional
@method_decorator(professional_required, name='dispatch')
class EventDeleteView(UserPassesTestMixin, DeleteView):
    model = Event
    template_name = "event_confirm_delete.html"
    # Redirect back to home page if deletion is successful
    success_url = '/'

    # Check if the authour making the delete request is the same as the one who created the event
    def test_func(self):
        event = self.get_object()
        if self.request.user == event.author:
            return True
        return False


@login_required
def event_book(request, pk):
    '''
    Book a spot to an event by replacing the current value of the field participants 
    to an modified version with the current user added to participants
    '''
    event = Event.objects.get(id = pk)
    event.value = event.participants.add(request.user)
    event.save()
    context = {
        'event' : event
    }
    return render(request, 'event_book_confirm.html', context)

@login_required
def event_unbook(request, pk):
    '''
    Unbook a spot to an event by replacing the current value of the field participants 
    to an modified version with the current user removed from participants
    '''
    event = Event.objects.get(id = pk)
    event.value = event.participants.remove(request.user)
    event.save()
    return redirect('event_detail', event.pk)

