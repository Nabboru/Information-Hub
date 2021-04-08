from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import DateField

#------------Library by Andrew Mackowski--------------------
from phonenumber_field.modelfields import PhoneNumberField
#-----------------------------------------------------------
class User(AbstractUser):
   email = models.EmailField(unique=True)
   username = models.CharField(max_length=30, blank=True, null = True)
   USERNAME_FIELD = 'email'
   first_name = models.CharField(max_length=30)
   dob = DateField(null = True)
   last_name = models.CharField(max_length=30)
   is_professional = models.BooleanField(default=False)
   is_patient = models.BooleanField(default=False)
   is_family  = models.BooleanField(default=False)
   phone_number = PhoneNumberField(blank=True)
   profile_picture = models.ImageField(blank=True)
   REQUIRED_FIELDS = ['username']
   
   def __str__(self):
      return (self.first_name + " " + self.last_name)
   
