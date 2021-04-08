from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Login URLs
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    #Signup URLs
    path('signup/', views.signup, name='signup'),
    path('signup/patient/<uidb64>/<token>/', views.SignupInviteView.as_view(template_name='signup_patient_invite.html'), name='patient-signup-with-invite'),
    path('signup/patient', views.SignUpView.as_view(template_name='signup_patient.html'), name='patient-signup'),
    path('signup/family/', views.SignUpView.as_view(template_name='signup_family.html'), name='family-signup'),
    path('signup/professional/', views.SignUpView.as_view(template_name='signup_health_prof.html'), name='healthprof-signup'),
    
    #Account activation URLs
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),

    #Password Reset URLs
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name = "password_reset.html"), name ='password-reset'),
    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(template_name = "password_reset_sent.html"), name ='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = "password_reset_form.html"), name ='password_reset_confirm'),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "password_reset_done.html"), name ='password_reset_complete'),

    #Profile URLs
    path('profile/', views.profile, name='user'),
    path('profile/edit/', views.UserUpdateView.as_view(), name='edit-user'),
    path('profile/delete-account/<pk>/', views.UserDeleteView.as_view(), name='delete-user'),

    #Invite user to signup
    path('send-invite/', views.InvitationView.as_view(), name='invite'),

]
