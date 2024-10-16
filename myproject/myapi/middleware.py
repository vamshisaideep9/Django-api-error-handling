import json
import logging
from django.http import JsonResponse

logger = logging.getLogger('myapi')

class ExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            logger.exception('Unhandled Exception %s', str(e))
            return JsonResponse({'error','Internal server error'}, status=500)

        