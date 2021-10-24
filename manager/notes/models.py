from django.db import models
from django.conf import settings


class Note(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field='id')

    text = models.TextField(max_length=128, unique=True)

    def __str__(self,):
        return str(self.id)
