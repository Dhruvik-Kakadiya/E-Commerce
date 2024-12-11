from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.conf import settings


def send_activation_email(user):
    token_generator = PasswordResetTokenGenerator()
    token = token_generator.make_token(user)
    uid = user.pk

    activation_link = f"{settings.FRONTEND_URL}/activate/{uid}/{token}/"

    subject = "Activate Your Account"
    message = f"Hi {user.username},\n\nPlease activate your account by clicking the link below:\n{activation_link}\n\nThank you!"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)
