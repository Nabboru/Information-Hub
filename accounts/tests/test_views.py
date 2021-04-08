from django import template
from django.http import response
from django.test import TestCase
from accounts.models import User
from django.core import mail
from django.urls import reverse
class LoginTestCase(TestCase):
    def setUp(self):
        user_email = 'testing@email.com'
        user = User.objects.create_superuser(username= 'test', email= user_email, password = '123')
        user.save()


    def test_user_login(self):
        response = self.client.post('/login/', {'username': 'testing@email.com', 'password': '123'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_wrong_credentials_login(self):
        response = self.client.post('/login/', {'username': 'z@email.com ', 'password': '123'})
        self.assertEqual(response.status_code, 200)

class PatientSignUpTestCase(TestCase): 
    def setUp(self):
        user_email = 'testing@email.com'
        user = User.objects.create_superuser(username= 'test', email= user_email, password = '123')
        user.save()
        self.client.login(username=user_email, password='123')

    def test_invite_email(self):
        response = self.client.get('/send-invite/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/send-invite/', {'email': 'testing@email.com'})
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Invite to signup')

    def test_valid_patient_user(self):
        response = self.client.post('/send-invite/', {'email': 'testing78907@email.com'})
        self.client.logout()
        token = response.context[0]['token']
        uid = response.context[0]['uid']
        response = self.client.get(reverse('patient-signup-with-invite', kwargs={'token':token,'uidb64':uid}))
        credentials ={
            'email': 'testing78907@email.com',
            'first_name': 'Leticia',
            'last_name': 'Piucco Marques',
            'dob': '1999-08-09',
            'password1': '654you789@',
            'password2': '654you789@',
            'is_patient': 'true'
        }
        response = self.client.post(reverse('patient-signup-with-invite', kwargs={'token':token,'uidb64':uid}), credentials)
        self.assertTemplateUsed(response, 'signup_email_verification.html')

    def test_user_with_invalid_field(self):
        response = self.client.post('/send-invite/', {'email': 'testing78907@email.com'})
        self.client.logout()
        token = response.context[0]['token']
        uid = response.context[0]['uid']
        response = self.client.get(reverse('patient-signup-with-invite', kwargs={'token':token,'uidb64':uid}))
        credentials ={
            'email': 'testing78907@email.com',
            'first_name': 'Leticia',
            'last_name': 'Piucco Marques',
            'dob': '1999-08-09',
            'password1': '654you789@',
            'password2': '',
            'is_patient': 'true'
        }
        response = self.client.post(reverse('patient-signup-with-invite', kwargs={'token':token,'uidb64':uid}), credentials)
        self.assertTemplateUsed(response, 'signup_patient_invite.html')


class FamilySignUpTestCase(TestCase):
    def test_valid_family_user(self):
        response = self.client.get('/signup/family/')
        self.assertEqual(response.status_code, 200)
        credentials ={
            'email': 'famtest@email.com',
            'first_name': 'Family',
            'last_name': 'Account',
            'dob': '1999-08-09',
            'password1': 'health678@',
            'password2': 'health678@',
        }
        response = self.client.post('/signup/family/', credentials)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup_email_verification.html')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Activate Your Account')
        token = response.context[0]['token']
        uid = response.context[0]['uid']
        # Now we can use the token to get the password change form
        response = self.client.get(reverse('activate', kwargs={'token':token,'uidb64':uid}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup_verified.html')


    def test_family_with_umatched_passwords(self):
        credentials ={
            'email': 'famtest@email.com',
            'first_name': 'Family',
            'last_name': 'Account',
            'dob': '1999-08-09',
            'password1': 'health68@',
            'password2': 'health678@',
        }
        response = self.client.post('/signup/family/', credentials)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup_family.html')

class ProfessionalSignUpTestCase(TestCase):
    def test_valid_professional_user(self):
        response = self.client.get('/signup/professional/')
        self.assertEqual(response.status_code, 200)
        credentials ={
            'email': 'proftest@nhs.net',
            'first_name': 'Healthcare professional',
            'last_name': 'Account',
            'dob': '1999-08-09',
            'password1': 'health678@',
            'password2': 'health678@',
        }
        response = self.client.post('/signup/professional/', credentials)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup_email_verification.html')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Activate Your Account')
        token = response.context[0]['token']
        uid = response.context[0]['uid']
        # Now we can use the token to get the password change form
        response = self.client.get(reverse('activate', kwargs={'token':token,'uidb64':uid}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup_verified.html')

    def test_professional_with_umatched_passwords(self):
        credentials ={
            'email': 'proftest@email.com',
            'first_name': 'Healthcare professional',
            'last_name': 'Account',
            'password1': 'health678@',
            'password2': 'health67@',
        }
        response = self.client.post('/signup/professional/', credentials)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup_health_prof.html')

class RestrictedViewsTestCase(TestCase):
    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/profile/')
        self.assertRedirects(response, '/login/?next=/profile/')

class PaswordRecoveryTestCase(TestCase):
    def setUp(self):
        credentials ={
            'email': 'proftest@nhs.net',
            'first_name': 'Healthcare professional',
            'last_name': 'Account',
            'dob': '1999-08-09',
            'password1': 'health678@',
            'password2': 'health678@',
        }
        response = self.client.post('/signup/professional/', credentials)
        token = response.context[0]['token']
        uid = response.context[0]['uid']
        self.client.get(reverse('activate', kwargs={'token':token,'uidb64':uid}))
    
    def test_password_recovery(self):
        self.assertEqual(len(mail.outbox), 1)
        response = self.client.get('/reset-password/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password_reset.html')

        response = self.client.post('/reset-password/', {'email':'proftest@nhs.net'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/reset-password-sent/')
        
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[1].subject, 'Password reset on testserver')

        token = response.context[1]['token']
        uid = response.context[1]['uid']
        response = self.client.get(reverse('password_reset_confirm', kwargs={'uidb64':uid, 'token':token}))
        response = self.client.post(reverse('password_reset_confirm', 
            kwargs={'uidb64':uid, 'token':token}), {'new_password1':'pass','new_password2':'pass'})
        self.assertEqual(response.status_code, 302)

class EditUserTestCase(TestCase):
    def setUp(self):
        user_email = 'testing@email.com'
        user = User.objects.create_superuser(username= 'test', email= user_email, password = '123')
        user.save()
        self.client.login(username=user_email, password='123')

    def test_edit_user(self):
        user = User.objects.get(email='testing@email.com')
        response = self.client.get('/profile/edit/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            '/profile/edit/', {'email':'email2@email.com', 'first_name': "Paul", 'last_name': 'Smith', 'dob': '1999-08-09'},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user'))
        user.refresh_from_db()
        self.assertEqual(user.email, "email2@email.com")
        self.client.logout()

        # Check if user can login with new email
        logged = self.client.login(username='email2@email.com', password='123')
        self.assertEqual(logged, True)
        self.client.logout()

        #Check if user cannot login with old email
        logged = self.client.login(username='testing@email.com', password='123')
        self.assertEqual(logged, False)
    
    def test_edit_user_empty_email(self):
        user = User.objects.get(email='testing@email.com')
        response = self.client.get(reverse('edit-user'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            '/profile/edit/', {'first_name': "Paul", 'last_name': 'Smith', 'dob': '1999-08-09', 'email':''},
        )
        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        self.assertNotEqual(user.email, '')

    def test_delete_user(self):
        user = User.objects.get(email='testing@email.com')
        response = self.client.get(reverse('delete-user', args=[user.pk]))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('delete-user', args=[user.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')