from django.core import exceptions


def validate_goal_category(category):
    if category not in ('personal', 'business', 'spiritual', 'relationship', 'family', 'community', 'physical'):
        raise exceptions.ValidationError('invalid goal category.')
