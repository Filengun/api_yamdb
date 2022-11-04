from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE = (
    ('admin', 'admin'),
    ('moderator', 'moderator'),
    ('user', 'user')
)


class User(AbstractUser):
    first_name = models.CharField(max_length=150, blank=True)
    role = models.CharField(max_length=20, choices=ROLE, default='USER')
    bio = models.CharField(
        max_length=1000, verbose_name='Биография', blank=True)
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
