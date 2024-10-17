from django.http import JsonResponse


class CustomApiException(Exception):

    status_code = 500
    default_detail = 'A custom Error occured.'

    def __init__(self, status_code = None, detail = None):
        self.detail = detail or self.default_detail
        if status_code:
            self.status_code = status_code

    def to_dict(self):
        return {'error': self.detail, 'code':self.detail}



class ItemNotFound(CustomApiException):
    status_code = 404
    default_detail = 'The required item was not found.'

class InvalidInput(CustomApiException):
    status_code = 400
    default_detail = 'Invalid input provided.'

class UnauthorizedAccess(CustomApiException):
    status_code = 401
    default_detail = 'Unauthorized Access.'