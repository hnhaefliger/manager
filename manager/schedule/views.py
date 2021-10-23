from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.core import exceptions

from datetime import datetime

from .models import Task
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    lookup_url_kwarg = 'task'

    def get(self, request, *args, **kwargs):
        data = Task.objects.filter(user_id=request.user)

        if 'before' in request.GET:
            try:
                data = data.filter(scheduled_for__lte=datetime.strptime(request.GET['before'], '%Y-%m-%d').date())

            except:
                raise exceptions.ValidationError('invalid before date.')

        if 'after' in request.GET:
            try:
                data = data.filter(scheduled_for__gte=datetime.strptime(request.GET['after'], '%Y-%m-%d').date())

            except:
                raise exceptions.ValidationError('invalid after date.')

        data = [{
            'id': task.id,
            'start': task.start,
            'end': task.end,
            'text': task.text,
            'task_type': task.task_type,
            'created_on': task.created_on,
            'scheduled_for': task.scheduled_for,
        } for task in data]

        return Response(data=data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        request.data.update({'user_id': request.user.id})
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        try:
            Task.objects.get(id=request.data['id']).delete()

        except:
            raise exceptions.ObjectDoesNotExist('invalid task id')

