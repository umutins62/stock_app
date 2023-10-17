from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404, reverse

class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin/') and not request.user.is_authenticated:
            return render(request, '404.html', status=404)
        return self.get_response(request)