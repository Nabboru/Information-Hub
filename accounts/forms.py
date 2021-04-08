from django.contrib.auth.forms import UserCreationForm, UserChangeForm, forms
from .models import User

#---------------------Library by Andrew Mackowski--------------------
from phonenumber_field.formfields import PhoneNumberField
#--------------------------------------------------------------------
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'dob', 'is_professional', 'phone_number', 'is_patient', 'is_family')
        labels = {
            'dob': ('Date of Birth'),
        }
    def clean(self):
        cleaned_data = super().clean()
        data = cleaned_data.get('email')
        data2 = cleaned_data.get('is_professional')
        if data2:
            if "@nhs.net" not in data:
                raise forms.ValidationError("Please use your NHS email")
                
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'dob', 'phone_number', 'profile_picture')


class InvitationForm(forms.Form):
    email = forms.EmailField() 
