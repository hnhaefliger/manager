from rest_framework.exceptions import *


class ConfirmationError(APIException):
    status_code = 401
    default_detail = 'your account is not confirmed.'
    default_code = '401'
