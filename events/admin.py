from django.contrib import admin
from .models import Event

# Register event model to provide admin CRUD operations
admin.site.register(Event)