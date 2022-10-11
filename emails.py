from django.core.mail import send_mail
from django.core.mail import EmailMessage

import random
from django.conf import settings
from .models import User



def send_otp_via_email(email):
    subject = f'Your acount verification email'
    otp = random.randint(1000, 9999)
    message = 'Your otp is : {}'.format(otp)
    email_from = settings.EMAIL_HOST 
    send_mail(subject, message, email_from , [email])
    user_obj = User.objects.get(email = email)
    user_obj.otp = otp
    user_obj.save()




