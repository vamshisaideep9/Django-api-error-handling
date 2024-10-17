import json
import logging
from django.http import JsonResponse
from .custom_exceptions import CustomApiException

logger = logging.getLogger('myapi')

class ExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
       response = self.get_response(request)
       return response
    
    def process_exception(self, request, exception):
        if isinstance(exception, CustomApiException):
            response_data = exception.to_dict()
            return JsonResponse(response_data, status = exception.status_code)
        return None
    


        