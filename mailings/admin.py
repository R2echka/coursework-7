from django.contrib import admin
from .models import MailingRecipient, Mailing, Message, MailingAttempt

# Register your models here.
@admin.register(MailingRecipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'name', 'comment')

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'owner')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject')

@admin.register(MailingAttempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'time', 'status', 'mailing', 'server_answer')