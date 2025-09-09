from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


@shared_task
def send_verification_email(user_id, verification_token):
    """
    Send email verification link to user.
    """
    from .models import User

    try:
        user = User.objects.get(id=user_id)
        verification_url = (
            f"{settings.FRONTEND_URL}/verify-email/{verification_token}/"
        )

        subject = 'Подтверждение email'
        message = render_to_string('emails/verification.txt', {
            'user': user,
            'verification_url': verification_url
        })

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
    except User.DoesNotExist:
        print(f"User with id {user_id} does not exist")