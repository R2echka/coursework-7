from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.utils import timezone
from config.settings import EMAIL_HOST_USER
from mailings.models import Mailing, MailingAttempt


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("mailing_pk", nargs="*", type=int)

    def handle(self, *args, **options):
        mailing = Mailing.objects.get(pk = options['mailing_pk'])
        for recipient in mailing.recipients.all():
            try:
                send_mail(
                    mailing.message.subject,
                    mailing.message.text,
                    from_email=EMAIL_HOST_USER,
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
                    status="unsuccsess",
                    server_answer=str(e),
                    mailing=mailing,
                )
        mailing.save()