from django import template
from django.test import TestCase
from accounts.forms import CustomUserCreationForm
from django.contrib.auth.forms import forms

class SignupFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'email': 'emailtest@email.com',
            'first_name': 'test',
            'last_name': 'test',
            'dob': '1980-09-09',
            'phone_number': '+4407751798570',
            'password1': 'testing123@',
            'password2': 'testing123@',
            'is_patient': 'true'
        }
        form = CustomUserCreationForm(form_data)
        self.assertTrue(form.is_valid())
    
    def test_valid_form_w_no_phone(self):
        form_data = {
            'email': 'emailtest@email.com',
            'first_name': 'test',
            'last_name': 'test',
            'dob': '1980-09-09',
            'password1': 'testing123@',
            'password2': 'testing123@',
        }
        form = CustomUserCreationForm(form_data)
        self.assertTrue(form.is_valid())
    
    def test_form_no_first_name(self):
        form_data = {
            'email': 'emailtest@email.com',
            'last_name': 'test',
            'dob': '1980-09-09',
            'phone_number': '+4407751798570',
            'password1': 'testing123@',
            'password2': 'testing123@',
        }
        form = CustomUserCreationForm(form_data)
        self.assertFalse(form.is_valid())
    
    def test_form_no_last_name(self):
        form_data = {
            'email': 'emailtest@email.com',
            'first_name': 'test',
            'dob': '1980-09-09',
            'phone_number': '+4407751798570',
            'password1': 'testing123@',
            'password2': 'testing123@',
        }
        form = CustomUserCreationForm(form_data)
        self.assertFalse(form.is_valid())

    def test_form_no_email(self):
        form_data = {
            'first_name': 'test',
            'last_name': 'test',
            'dob': '1980-09-09',
            'phone_number': '+4407751798570',
            'password1': 'testing123@',
            'password2': 'testing123@',
            'is_patient': 'true'
        }
        form = CustomUserCreationForm(form_data)
        self.assertFalse(form.is_valid())

    def test_form_no_password_confirmation(self):
        form_data = {
            'first_name': 'test',
            'last_name': 'test',
            'dob': '1980-09-09',
            'phone_number': '+4407751798570',
            'password1': 'testing123@',
        }
        form = CustomUserCreationForm(form_data)
        self.assertFalse(form.is_valid())

    def test_form_no_password(self):
        form_data = {
            'first_name': 'test',
            'last_name': 'test',
            'dob': '1980-09-09',
            'phone_number': '+4407751798570',
            'password2': 'testing123@',
        }
        form = CustomUserCreationForm(form_data)
        self.assertFalse(form.is_valid())
    
    def test_professional_no_nhs_email(self):
        form_data = {
            'email': 'emailtest@email.com',
            'first_name': 'test',
            'last_name': 'test',
            'dob': '1980-09-09',
            'phone_number': '+4407751798570', 
            'password1': 'testing123@',
            'password2': 'testing123@',
            'is_professional': 'true'
        }
        form = CustomUserCreationForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertRaisesMessage(form.errors, forms.ValidationError)
        self.assertRaisesMessage(form.errors, 'Please use your nhs email to signup')