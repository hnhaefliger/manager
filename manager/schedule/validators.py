from django.core import exceptions


def validate_task_type(task_type):
    if task_type not in ('breakout', 'buffer', 'strategic'):
        raise exceptions.ValidationError('invalid task type.')


def validate_time(time):
    if not(time >= 0 and time <= 1440):
        raise exceptions.ValidationError('invalid time.')
