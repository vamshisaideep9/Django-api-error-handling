from django.http import JsonResponse

def error_message(message, status=400):
    return JsonResponse({'error':message}, status = status)