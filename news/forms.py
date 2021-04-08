# import form class from django
from django import forms
from django.forms import DateTimeInput

# import News from models.py
from .models import News

class NewsForm(forms.ModelForm):
    class Meta:
        model = News

        fields = ['title', 'content']

        def __init__(self, *args, **kwargs):
            super(NewsForm, self).__init__(*args, **kwargs)
