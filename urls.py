
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from accounts.views import *

urlpatterns = [
    path('register/', RegisterAPI.as_view()),
    path('verify/', VerifyOTP.as_view()),
    path('sentotp/', VerifyEmailAPI.as_view()),
    path('resetpassword/', SetNewPasswordAPI.as_view()),
    
    path('admin/', admin.site.urls),
#Reset Password
#  path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
#  path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),



    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), 
        name="password_reset_done"),


    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), 
        name="password_reset_complete"),
]
