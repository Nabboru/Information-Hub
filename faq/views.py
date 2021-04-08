from django.shortcuts import render
from faq.models import FAQPost
from django.views.generic import ListView

# The views for the FAQ
def faq(request):
    context = {
        'faq': FAQPost.objects.all().order_by('-last_modified')
    }
    return render(request, 'FAQ.html', context)
