from rest_framework import serializers
from django.core import exceptions
from django.conf import settings

from .models import Note
from authentication.models import User


class NoteSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    text = serializers.CharField()

    def create(self, validated_data):
        return Note.objects.create(
            user_id=validated_data['user_id'],

            text=validated_data['text'],
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

        return data
