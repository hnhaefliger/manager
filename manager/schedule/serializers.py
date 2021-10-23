from rest_framework import serializers
from django.core import exceptions
from django.conf import settings

from datetime import datetime, time, timedelta

from .models import Task
from .validators import validate_task_type, validate_time
from authentication.models import User


class TaskSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    start = serializers.IntegerField(validators=[validate_time])
    end = serializers.IntegerField(validators=[validate_time])

    text = serializers.CharField()
    task_type = serializers.CharField(validators=[validate_task_type])

    scheduled_for = serializers.CharField()

    def create(self, validated_data):
        return Task.objects.create(
            user_id=validated_data['user_id'],

            start=validated_data['start'],
            end=validated_data['end'],

            text=validated_data['text'],
            task_type=validated_data['task_type'],

            created_on=validated_data['created_on'].date(),
            scheduled_for=validated_data['scheduled_for'].date(),
        )

    """
    def update(self, instance, validated_data):
        '''
        Update a user's data.
        '''
        return instance
    """

    def validate(self, data):
        try:
            data['user_id'] = User.objects.get(id=data['user_id'])

        except:
            raise exceptions.ObjectDoesNotExist('invalid user id')

        print(data)
        if data['start'] > data['end']:
            raise exceptions.ValidationError('task must start before it ends.')

        data['created_on'] = datetime.combine(datetime.today(), time.min)

        try:
            data['scheduled_for'] = datetime.strptime(data['scheduled_for'], '%Y-%m-%d')

        except:
            raise exceptions.ValidationError('invalid date.')

        # prevent overlapping tasks

        return data
