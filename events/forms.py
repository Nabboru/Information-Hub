# import form class from django 
from django import forms 
from django.forms import DateTimeInput
  
# import Event from models.py 
from .models import Event 

'''
Form for creating and updating events with a specific format(such as "2021-03-30T17:30") for the start and end time, creation_time is generated automatically and the author is inferred from the session
'''
class EventForm(forms.ModelForm): 
    class Meta: 
        model = Event 
        widgets = {
            'start_time': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%d %H:%M'),
            'end_time': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%d %H:%M')
        }
        fields = ['subject', 'content', 'start_time', 'end_time', 'url', 'location']

        def __init__(self, *args, **kwargs):
            super(EventForm, self).__init__(*args, **kwargs)
            self.input_formats = ("%Y-%m-%d %H:%M",)+(self.input_formats)


