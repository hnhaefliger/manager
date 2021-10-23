from rest_framework import exceptions

from .models import Token
from .utils import hash_token, get_authorization_header


class BaseAuthentication:
    '''
    Base authentication class for inheritance.
    '''

    def authenticate(self, request):
        '''
        Authenticate a request.
        '''
        raise NotImplementedError(".authenticate() must be overridden.")

    def authenticate_header(self, request):
        ''''
        Return the keyword for this backend.
        '''
        pass


class AuthenticationBackend(BaseAuthentication):
    '''
    Custom authentication backend.
    '''
    keyword = 'Token'
    model = Token

    def authenticate(self, request):
        '''
        Verify that the request token is valid.
        '''
        auth = get_authorization_header(request).split()

        # if the authentication header is invalid for this backend
        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:  # correct backend but invalid token
            raise exceptions.AuthenticationFailed('no token provided.')

        elif len(auth) > 2:  # correct backend but invalid token
            raise exceptions.AuthenticationFailed('token string should not contain spaces.')

        try:
            token = auth[1].decode()

        except UnicodeError:
            raise exceptions.AuthenticationFailed('token string should not contain invalid characters.')

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        '''
        Validate a token with the database.
        '''
        try:
            token = self.model.objects.select_related('user_id').get(token=hash_token(key))

        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed('invalid token.')

        if not token.user_id.is_active:
            raise exceptions.AuthenticationFailed('invalid token')

        if not token.user_id.confirmed:
            raise exceptions.AuthenticationFailed('this account has not been confirmed yet.')

        return (token.user_id, token)

    def authenticate_header(self, request):
        '''
        Return the keyword used to determine authentication backend.
        '''
        return self.keyword
