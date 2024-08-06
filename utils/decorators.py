import json
from functools import wraps

from django.http import HttpResponseBadRequest

def use_body(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.body:
            return HttpResponseBadRequest()
        body = json.loads(request.body)
        return func(request, *args, **kwargs, body=body)
    
    return wrapper