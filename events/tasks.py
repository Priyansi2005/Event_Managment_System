from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_rsvp_email(user_email, event_title):
    send_mail(
        subject=f"RSVP Confirmed for {event_title}",
        message=f"You have successfully RSVP'd to {event_title}.",
        from_email='noreply@example.com',
        recipient_list=[user_email],
        fail_silently=False
    )
