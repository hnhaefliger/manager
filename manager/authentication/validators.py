from django.core import validators
from django.contrib.auth import password_validation

from .models import User
from . import exceptions


def validate_email(email):
    validators.validate_email(email)

    if User.objects.filter(email=email).exists():
        raise exceptions.ValidationError('email is already in use.')


def validate_name(name):
    validators.RegexValidator(validators._lazy_re_compile(r'^[-a-zA-Z0-9-\']+\Z'), 'name contains invalid characters.')(name)


def validate_password(password):
    password_validation.validate_password(password)
