from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.views.generic.edit import FormView
from .tokens import account_activation_token, default_token_generator
from .forms import CustomUserCreationForm, InvitationForm, CustomUserChangeForm
from .models import User
from forum.models import ForumPost
from events.models import Event
from .decorators import professional_required

def signup(request):
    """
    Shows the different types of signups 
    """
    return render(request, 'signup_options.html')

class SignUpView(CreateView):
    """
    Signup for relatives and professionals.
    """
    form_class = CustomUserCreationForm
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            return render(request,'signup_email_verification.html')

        return render(request, self.template_name, {'form': form})

class SignupInviteView(CreateView):
    """
    Signup for patients with the email invite.
    """
    form_class = CustomUserCreationForm
    def post(self, request, uidb64, token):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            return render(request,'signup_email_verification.html')
        return render(request, self.template_name, {'form': form})    


def activate(request, uidb64, token):
    '''
    activate an user account when the token is valid
    '''
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        return render(request, 'signup_verified.html')
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'signup_verified.html')
    return render(request, 'signup_verified.html')

@login_required
def profile(request):
    """
    View of user information and their posts and events
    """
    context = {
        'posts': ForumPost.objects.filter(username = request.user.id),
        'events': Event.objects.filter(author = request.user.id)
    }
    return render(request, 'user_profile.html', context)


@method_decorator(login_required(login_url='/'), name='dispatch')
class UserUpdateView(UpdateView):
    """
    Edit user view
    """
    form_class = CustomUserChangeForm
    template_name = 'user_edit.html'
    success_url = reverse_lazy('user')
    
    def get_object(self):
        '''
        Get the current logged in user
        '''
        return self.request.user

@method_decorator(login_required(login_url='/'), name='dispatch')
class UserDeleteView(DeleteView):
    """
    Delete user view
    """
    model = User
    template_name = "user_delete.html"

    # Redirect back to home page if deletion is successful
    success_url = '/'

    def get_object(self):
        return self.request.user
    
@method_decorator(professional_required(), name='dispatch')
class InvitationView(FormView):
    """
    Send patients a invite via email to signup.
    """
    form_class = InvitationForm
    template_name = "invite_patient.html"
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = user = User.objects.get_or_create(username='whatever')[0]
            current_site = get_current_site(request)
            # Email 
            subject = 'Invite to signup'
            message = render_to_string('invite_patient_email.html', {
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user)),
                'token': default_token_generator.make_token(user),
            })
            send_mail(subject, message, None, [email])

        return render(request, self.template_name, {'form': form})