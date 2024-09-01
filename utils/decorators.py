import json
from functools import wraps

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

def use_body(*fields: str):
    
    def decorator(func):
        @wraps(func)
        def wrapper(request, **kwargs):
            if not request.body:
                return JsonResponse({'error': 'ERR_MISSING_FIELD'})
            body = json.loads(request.body)

            for name in fields:
                if name not in body:
                    return JsonResponse({'error': 'ERR_MISSING_FIELD'})
            
            return func(request, **kwargs, body=body)
        
        return wrapper
    return decorator

def use_params(*fields: str):
    def decorator(func):
        @wraps(func)
        def wrapper(request, **kwargs):
            if not request.GET:
                return JsonResponse({'error': 'ERR_MISSING_FIELD'})
            for name in fields:
                if name not in request.GET:
                    return JsonResponse({'error': 'ERR_MISSING_FIELD'})
            
            params = request.GET
            return func(request, **kwargs, params=params)
        
        return wrapper
    return decorator