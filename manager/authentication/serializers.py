from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

from rest_framework import serializers

from . import exceptions
from .validators import validate_name, validate_email, validate_password
from .utils import hash_token, create_token
from .models import User, Token


class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField(validators=(validate_name,))
    last_name = serializers.CharField(validators=(validate_name,))

    email = serializers.CharField(validators=(validate_email,))

    password = serializers.CharField(validators=(validate_password,))

    def create(self, validated_data):
        return User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],

            email=validated_data['email'],

            password=validated_data['password'],
        )

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance

    def validate(self, data):
        data['password'] = make_password(data['password'])

        return data


class TokenSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def save(self):
        super().save()

        return self.validated_data['token']

    def create(self, validated_data):
        return Token.objects.create(
            user_id=validated_data['user_id'],
            token=hash_token(validated_data['token'])
        )

    def validate(self, data):
        user = authenticate(
            email=data['email'],
            password=data['password'],
        )

        if not user:
            raise exceptions.AuthenticationFailed('invalid credentials.')

        elif not user.confirmed:
            raise exceptions.ConfirmationError('this account has not been confirmed yet.')

        else:
            data['user_id'] = user
            data['token'] = create_token()
            return data
