from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
import random
import string

def generate_verification_code(length=6):
    characters = string.digits  # Use digits (0-9) for the verification code
    code = ''.join(random.choice(characters) for _ in range(length))
    return code




def send_verification_email(code,email="mohamedhani590@gmail.com"):
    msg_html = render_to_string('email_verification_code.html',{"code":code})
    msg_plain = render_to_string('email_verification_code.txt', {'code': code})
    email = send_mail(
        'Verification Code',
        msg_plain,
        settings.EMAIL_HOST_USER, 
        [email],
        html_message=msg_html,  
    )
