from django.db import models
from django.conf import settings


class Goal(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field='id')

    text = models.CharField(max_length=128, unique=True)
    category = models.CharField(max_length=64, unique=False)

    created_on = models.DateField()
    scheduled_for = models.DateField()

    def __str__(self,):
        return str(self.id)
