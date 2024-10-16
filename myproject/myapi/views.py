from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .models import Item
from .utils import error_message
import json
import logging

logger = logging.getLogger('myapi')
# Create your views here.
"""
request = GET. fetching data from the server/database
request = POST. submit data to the server to create or update a resource
request = PUT. update an existing data with the new data
"""

"""
@csrf_exempt is used to bypass the protection. When an api or view recieves requests from a 
client  or external system that cannot include CSRF token, we should use
@csrf_exempt to prevent django from blocking the request.
"""

    

#function based views
@csrf_exempt
def hello_api(request):
    if request.method == 'GET':
        data = {'message':'Hello, world!'}
        return JsonResponse(data)
    elif request.method == 'POST':
        try:
            body = json.loads(request.body)
            name = body.get('name','world')
            data = {'message' : f'Hello, {name}'}
            return JsonResponse(data, status = 201)
        except json.JSONDecodeError:
            return JsonResponse({'error':'Invalid Json'}, status=400)
    else:
        return JsonResponse({'error':'Method Not allowed'}, status=405)
    

"""
  200: OK. The request was successful and the response body contains requested data
  201: CREATED. The request was successful and new resource was created.(commonly used for POST request)
  202: ACCEPTED. The request has been accepted for processing, but the processing has not been completed yet.
  204: NO CONTENT. The request has been successful, But their is no content to send in the response.
"""

"""
   400: BAD REQUEST. The server cannot process the request due to client error.(invalid syntax)
   401: UNAUTHORIZED. Authentication is required and has failed or not yet been provided.
   403: FORBIDDEN. Server understood the request but refuses to authorize it.
   404: NOT FOUND: The server cannot find the request resource.(page not found)
   408: SERVER TIMEOUT. The server timedout waiting for the request.
"""

"""
   500: INTERNAL SERVER ERROR. something has gone wrong in the server.
   502: BAD GATEWAY. The server while acting as a gateway or proxy, received an invalid 
   response from an inbound server.
"""

#class based view

@method_decorator(csrf_exempt, name='dispatch')
class HelloApiView(View):
    def get(self, request):
        data = {'message': 'Hello, world!'}
        return JsonResponse(data)
    
    def post(self, request):
        try:
            body = json.loads(request.body)
            name = body.get('name','world')
            data = {'message': f'Hello, {name}'}
            return JsonResponse(data, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error':'Invalid Json'}, status=400)
        
@method_decorator(csrf_exempt, name='dispatch')
class ItemListView(View):
    #converting model into json serializable
    def get(self, request):
        logger.info("Fetching all items")
        items = Item.objects.all()
        data = {
            'items': [
                {
                    'id' : item.id,
                    'name' : item.name,
                    'slug' : item.slug,
                    'description' : item.description,
                    'created_at' : item.created_at.isoformat()
                } for item in items
            ]
        }
        return JsonResponse(data)
    
    def post(self, request):
        logger.info('Creating a New item')
        try:
            body = json.loads(request.body)
            name = body['name']
            description = body['description']
            item = Item.objects.create(name=name, description=description)
            data = {
            'id' : item.id,
            'name' : item.name,
            'slug' : item.slug,
            'description' : item.description,
            'created_at' : item.created_at.isoformat(),
            }
            logger.info("Item created with slug %s", item.slug)
            return JsonResponse(data, status=201)
        except KeyError as e:
            logger.warning("Missing Field: %s", e.args[0])
            return error_message(f'Missing Field: {e.args[0]}', status=400)
        except json.JSONDecodeError:
            logger.warning('Invalid Json in request body')
            return error_message('Invalid Json', status=400)
        except Exception as e:
            logger.error('Error creating item: %s', str(e))
            return error_message('Internal Server Error', status=500)

@method_decorator(csrf_exempt, name='dispatch')
class ItemDetailView(View):
    def get(self, request, slug):
        logger.info('Fetching item with slug %s', slug)
        try: 
            item = Item.objects.get(slug=slug)
            data = {
                'id':item.id,
                'name' : item.name,
                'slug' : item.slug,
                'description' : item.description,
                'created_at' : item.created_at.isoformat(),
            }
            return JsonResponse(data)
        except Item.DoesNotExist:
            logger.warning("Item with slug %s not found", slug)
            return error_message('Item not found', 404)
        except Exception as e:
            logger.error('Error Fetching item: %s', str(e))
            return error_message('Internal Server Error', 500)
        
    def delete(self, request, slug):
        logger.info('Deleting item with slug %s', slug)
        try:
            item = Item.objects.get(slug=slug)
            item.delete()
            return JsonResponse({'message':'Item deleted'}, status = 204)
        except Item.DoesNotExist:
            logger.warning('logger with slug %s not found', slug)
            return error_message('Item not found', 404)
        except Exception as e:
            logger.error('Error deleting item: %s', str(e))
            return error_message('Internal server error', 500)

    






