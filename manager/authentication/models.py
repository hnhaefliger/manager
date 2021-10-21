from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    '''
    Custom user model.
    '''
    first_name = models.CharField(max_length=128, blank=True)
    last_name = models.CharField(max_length=128, blank=True)

    email = models.EmailField(max_length=256, unique=True)
    password = models.CharField(max_length=128)

    confirmed = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_username(self):
        return self.email

    def __str__(self):
        return self.email


class Token(models.Model):
    '''
    Custom token model.
    '''
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='email')

    token = models.CharField(max_length=64, unique=True)

    valid_until = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self,):
        return self.token
