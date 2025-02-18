from django.db import models
from users.models import CustomUser

# Create your models here.
class MailingRecipient(models.Model):
    email = models.EmailField(unique=True, verbose_name='Email')
    name = models.CharField('ФИО', max_length=50)
    comment = models.TextField('Комментарий', blank=True, null=True)

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = 'Получатель рассылки'
        verbose_name_plural = 'Получатели рассылки'

class Message(models.Model):
    subject = models.CharField('тема письма', max_length=50)
    text = models.TextField('тело письма')

    def __str__(self):
        return self.subject
    
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

class Mailing(models.Model):
    CHOICES = [('created', 'создана' ),
    ('active','запущена'),
    ('completed','завершена')]

    starting_time = models.DateTimeField('Дата и время первой отправки', blank=True, null=True)
    ending_time = models.DateTimeField('Дата и время окончания отправки', blank=True, null=True)
    status = models.CharField('Статус рассылки', choices=CHOICES, default='created', max_length=20)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    recipients = models.ManyToManyField(MailingRecipient)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.pk
    
    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [('can_disable_mailing', 'Can disble mailing'),]

class MailingAttempt(models.Model):
    CHOICES = [('success','успешно'),
    ('unsuccsess','неуспешно')]

    time = models.DateTimeField('Дата и время попытки')
    status = models.CharField('Статус попытки', choices=CHOICES, default='success', max_length=20)
    server_answer = models.TextField('Ответ почтового сервера')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылок'