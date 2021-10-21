import binascii
import hashlib
import os
import uuid

from rest_framework import HTTP_HEADER_ENCODING


def hash_token(token):
    '''
    Hash a token so that plaintext tokens are not stored in the database.
    '''
    return hashlib.sha256(bytes(token, encoding='utf-8')).hexdigest()


def create_uuid():
    '''
    Generate a id that can be openly used to make indexing more difficult.
    '''
    return uuid.uuid4().hex


def create_token():
    '''
    Generate a user authentication token.
    '''
    return binascii.hexlify(os.urandom(20)).decode()


def get_authorization_header(request):
    '''
    Get and clean up the http authorization header.
    '''
    auth = request.META.get('HTTP_AUTHORIZATION', b'')  # get authentication header

    if isinstance(auth, str):
        auth = auth.encode(HTTP_HEADER_ENCODING)

    return auth
