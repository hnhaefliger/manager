from django.db import models
from django.conf import settings


class Task(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field='id')

    start = models.IntegerField()
    end = models.IntegerField()

    text = models.CharField(max_length=128, unique=True)
    task_type = models.CharField(max_length=64, unique=False)

    created_on = models.DateField()
    scheduled_for = models.DateField()

    def __str__(self,):
        return str(self.id)
