from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE = (
    ('ADMIN', 'admin'),
    ('MODERATOR', 'moderator'),
    ('USER', 'user')
)


class User(AbstractUser):
    first_name = models.CharField(max_length=150, blank=True)
    role = models.CharField(choices=ROLE, max_length=50, default='USER') #даша: max_length=50, чтобы запустился сервак
    bio = models.CharField(verbose_name='Биография', max_length=1024, blank=True) #даша: max_length=1024, чтобы запустился сервак
    email = models.EmailField(
        max_length=254,
        unique=True,
        error_messages={
            'unique': 'Такой email уже зарегистрирован.',
            'blank': 'Это поле обязательно для заполнения.'
        },
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
