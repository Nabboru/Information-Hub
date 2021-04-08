from django.forms import ModelForm, DateInput
from calendars.models import CalendarEvent

class CalendarEventForm(ModelForm):
  class Meta:
    model = CalendarEvent
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%d %H:%M'),
      'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%d %H:%M'),
    }
    fields = '__all__'

  def __init__(self, *args, **kwargs):
    super(CalendarEventForm, self).__init__(*args, **kwargs)
    # input_formats parses HTML5 datetime-local input to datetime field
    self.fields['start_time'].input_formats = ('%Y-%m-%d %H:%M',)
    self.fields['end_time'].input_formats = ('%Y-%m-%d %H:%M',)
