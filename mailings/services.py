from .models import Mailing
from django.core.mail import send_mail
from django.utils import timezone
from config.settings import EMAIL_HOST_USER
from mailings.models import Mailing, MailingAttempt, MailingRecipient
from config.settings import CACHE_ENABLED
from django.core.cache import cache

def active_mailings_number(user):
    mailings = Mailing.objects.filter(status = 'active')
    mailings = mailings.filter(owner_id = user.pk)
    return mailings.count()

def send_mailing(pk, user):
    mailing = Mailing.objects.get(pk = pk)
    for recipient in mailing.recipients.all():
        try:
            send_mail(
                mailing.message.subject,
                mailing.message.text,
                from_email=user.email,
                recipient_list=[recipient.email],
                fail_silently=False,
            )
            MailingAttempt.objects.create(
                time=timezone.now(),
                status="success",
                server_response="200",
                mailing=mailing,
            )
        except Exception as e:
            MailingAttempt.objects.create(
                time=timezone.now(),
                status="unsuccess",
                server_answer=str(e),
                mailing=mailing,
            )
    mailing.save()

def successful_attempts(user):
        mailings = Mailing.objects.filter(owner=user.pk)
        success_count = MailingAttempt.objects.filter(mailing__in=mailings, status='success').count()
        return success_count

def unsuccessful_attempts(user):
        mailings = Mailing.objects.filter(owner=user.pk)
        unsuccess_count = MailingAttempt.objects.filter(mailing__in=mailings, status='unsuccess').count()
        return unsuccess_count

def messages_count(user):
        mailings = Mailing.objects.filter(owner=user.pk).exclude(status='created')
        messages_count = mailings.values('message').distinct().count()
        return messages_count

def unique_recipients(user):
        return MailingRecipient.objects.filter(mailing__owner=user.pk).distinct().count()

def get_cached_mailings():
    if not CACHE_ENABLED:
        return Mailing.objects.all()
    key = 'mailings'
    mailings = cache.get('mailings')
    if mailings:
        return mailings
    mailings = Mailing.objects.all()
    cache.set(key, mailings)
    return mailings
