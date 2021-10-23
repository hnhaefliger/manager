from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from . import exceptions
from .models import User, Token
from .serializers import TokenSerializer, UserSerializer
from .utils import get_authorization_header, hash_token


class UserViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)
    lookup_url_kwarg = 'user'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response(data={
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'date_joined': request.user.date_joined,
            }, status=status.HTTP_200_OK)

        else:
            raise exceptions.NotAuthenticated('you are not logged in.')

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if 'old_password' in request.data:
                if request.user.check_password(request.data['old_password']):
                    serializer = UserSerializer(request.user, data=request.data, partial=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()

                    return Response(status=status.HTTP_200_OK)

                else:
                    raise exceptions.AuthenticationFailed('invalid credentials.')

            else:
                raise exceptions.AuthenticationFailed('you must provide a password to change your password.')

        else:
            raise exceptions.NotAuthenticated('you are not logged in.')

    def delete(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if 'password' in request.data:
                if request.user.check_password(request.data['password']):
                    request.user.is_active = False
                    request.user.save()

                    return Response(status=status.HTTP_204_NO_CONTENT)

                else:
                    raise exceptions.AuthenticationFailed('invalid credentials.')

            else:
                raise exceptions.AuthenticationFailed('you must provide a password to delete your account.')

        else:
            raise exceptions.NotAuthenticated('you are not logged in.')


class TokenViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        '''
        Get a new token for a user
        '''
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.save()

        return Response(data={'token': token}, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        auth = get_authorization_header(request).split()

        if auth and len(auth) == 2 and auth[0] == b'Token':
            try:
                token = Token.objects.get(token=hash_token(auth[1].decode()))

                if request.data['all']:  # sign out of all devices
                    tokens = Token.objects.filter(user=token.user)

                    for token in tokens:
                        token.delete()

                else:  # sign out of one device
                    token.delete()

                return Response(data=None, status=status.HTTP_204_NO_CONTENT)

            except:
                raise exceptions.AuthenticationFailed('invalid token.')

        else:
            raise exceptions.AuthenticationFailed('invalid authorization header.')
