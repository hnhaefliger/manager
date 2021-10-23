from rest_framework import serializers
from django.core import exceptions
from django.conf import settings

from datetime import datetime, time, timedelta

from .models import Goal
from .validators import validate_goal_category
from authentication.models import User


class GoalSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    text = serializers.CharField()
    category = serializers.CharField(validators=[validate_goal_category])

    scheduled_for = serializers.CharField()

    def create(self, validated_data):
        return Goal.objects.create(
            user_id=validated_data['user_id'],

            text=validated_data['text'],
            category=validated_data['category'],

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

        data['created_on'] = datetime.combine(datetime.today(), time.min)
        
        try:
            data['scheduled_for'] = datetime.strptime(data['scheduled_for'], '%Y-%m-%d')

        except:
            raise exceptions.ValidationError('invalid date.')

        return data
