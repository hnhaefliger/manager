from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.core import exceptions

from .models import Note
from .serializers import NoteSerializer


class NoteViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    lookup_url_kwarg = 'note'

    def get(self, request, *args, **kwargs):
        data = Note.objects.filter(user_id=request.user)

        data = [{
            'id': note.id,
            'text': note.text,
        } for note in data]

        return Response(data=data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        request.data.update({'user_id': request.user.id})
        serializer = NoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        try:
            Note.objects.get(id=request.data['id']).delete()

        except:
            raise exceptions.ObjectDoesNotExist('invalid task id')
