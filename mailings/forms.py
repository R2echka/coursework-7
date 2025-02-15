from django import forms
from django.core.exceptions import ValidationError
from .models import MailingRecipient, Message, Mailing

class RecipientForm(forms.ModelForm):
    class Meta:
        model = MailingRecipient
        fields = ['email', 'name', 'comment']
    
    def __init__(self, *args, **kwargs):
        super(RecipientForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите email получателя'})
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите ФИО получателя'})
        self.fields['comment'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Добавьте свой комментарий'})

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'text']
    
    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        self.fields['subject'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Тема письма'})
        self.fields['text'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Тело письма'})

class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['message', 'recipients']
    
    def __init__(self, *args, **kwargs):
        super(MailingForm, self).__init__(*args, **kwargs)

        self.fields['message'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Сообщение расслыки'})
        self.fields['recipients'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Выберите получателей'})