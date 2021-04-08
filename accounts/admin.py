from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['email', 'username', 'first_name', 'last_name', 'dob', 'is_patient', 'is_professional', 'phone_number', 'profile_picture']

admin.site.register(User, CustomUserAdmin)