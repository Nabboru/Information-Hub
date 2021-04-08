from django.shortcuts import render
from help_support.models import HelpSupportPost
from django.views.generic import ListView

# The views for the help and support page
def help_support(request):
    context = {
        'help_support': HelpSupportPost.objects.all().order_by('-last_modified')
    }
    return render(request, 'help_support.html', context)
