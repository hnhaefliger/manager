from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.core import exceptions

from .models import Goal
from .serializers import GoalSerializer


class GoalViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    lookup_url_kwarg = 'goal'

    def get(self, request, *args, **kwargs):
        data = Goal.objects.filter(user_id=request.user)

        # filter by date

        data = [{
            'id': goal.id,
            'text': goal.text,
            'category': goal.category,
            'created_on': goal.created_on,
            'scheduled_for': goal.scheduled_for,
        } for goal in data]

        return Response(data=data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        request.data.update({'user_id': request.user.id})
        serializer = GoalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        try:
            Goal.objects.get(id=request.data['id']).delete()

        except:
            raise exceptions.ObjectDoesNotExist('invalid goal id')
