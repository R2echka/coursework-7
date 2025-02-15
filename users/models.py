from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    username = models.CharField('Имя пользователя', max_length=20)
    email = models.EmailField(unique=True, verbose_name='Email')
    mailings = models.IntegerField('Количество рассылок', default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [('manager', 'Manager'),('can_block_users', 'Can block users')]

    def __str__(self):
        return self.email