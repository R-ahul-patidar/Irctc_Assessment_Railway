# railway/middleware.py
from django.http import JsonResponse
from django.conf import settings

class AdminAPIMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request is for an admin API endpoint
        if request.path.startswith('/api/admin/'):
            api_key = request.headers.get('API-Key')
            if api_key != settings.ADMIN_API_KEY:
                return JsonResponse({'error': 'Forbidden'}, status=403)
        
        response = self.get_response(request)
        return response
