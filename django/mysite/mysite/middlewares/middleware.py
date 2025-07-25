# middleware.py
from django.shortcuts import redirect
from django.http import Http404

class Custom404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            return redirect('error-404-1')
        return response