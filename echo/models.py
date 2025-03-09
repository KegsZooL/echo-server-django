from django.db import models
from django.contrib.auth.models import AbstractUser

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    published_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title


class CustomUser(AbstractUser):

    ROLE_CHOICES = [
            ('user', 'Пользователь'),
            ('admin', 'Администратор'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

