import time
from django.utils.deprecation import MiddlewareMixin
from .models import Log
from django.utils import timezone


class LoggingMiddleware(MiddlewareMixin):

    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        duration = time.time() - request.start_time
        if request.path.startswith('/admin'):
            return response

        Log.objects.create(
            path=request.path,
            method=request.method,
            status_code=response.status_code,
            duration=duration,
            timestamp=timezone.now()
        )
        return response
