from rest_framework.exceptions import APIException
from rest_framework import status


class DefaultException(APIException):
    default_code = 'invalid'
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {'code': status_code,
                      'message': 'Error.'}

    def __init__(self, detail=None, status_code=None):
        self.detail = detail if detail is not None else self.default_detail
        self.status_code = status_code if status_code is not None else self.status_code


class AlreadyExist(DefaultException):
    default_detail = {'code': DefaultException.status_code,
                      'detail': 'Active order with this bike is already exist.'}


class InvalidParam(DefaultException):
    default_detail = {'code': DefaultException.status_code,
                      'detail': 'Invalid or non-existent parameter has been passed.'}


class AlreadyOccupied(DefaultException):
    default_detail = {'code': DefaultException.status_code,
                      'detail': 'This bike place is already occupied.'}


class DoesntExists(DefaultException):
    default_detail = {'code': DefaultException.status_code,
                      'detail': 'Requested object doesn\'t exists'}


class Forbidden(DefaultException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {'code': status.HTTP_403_FORBIDDEN,
                      'detail': 'Forbidden.'}


class NotEnoughMoney(DefaultException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = {'code': status.HTTP_403_FORBIDDEN,
                      'detail': 'Not enough money or account has been blocked.'}
