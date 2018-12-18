import json
import os
import urllib3
from django.conf import settings
from django.http import JsonResponse
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_500_INTERNAL_SERVER_ERROR


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.AUTH_DEBUG_MODE is True:
            return self.get_response(request)

        if request.method == "POST" or request.method == "DELETE" or request.method == "PUT":
            auth = request.META.get("HTTP_AUTHORIZATION", None)

            if not auth or len(auth.split()) != 2:
                return JsonResponse({"Error": "Unauthenticated"}, status=HTTP_401_UNAUTHORIZED)

            parts = auth.split()
            token = parts[1]
            http = urllib3.PoolManager()

            auth_response = http.request(
                'GET',
                os.getenv('AUTH0_URL', ''),
                headers={
                    'Authorization': 'Bearer ' + token,
                    'Content-Type': 'application/json'
                }
            )

            if not auth_response.status == HTTP_200_OK:
                if auth_response.status == HTTP_403_FORBIDDEN or auth_response.status == HTTP_401_UNAUTHORIZED:
                    return JsonResponse({"Error": "Unauthorized"}, status=HTTP_401_UNAUTHORIZED)
                else:
                    return JsonResponse({"Error": "Internal Server Error"}, status=HTTP_500_INTERNAL_SERVER_ERROR)

            if request.method == "POST" or request.method == "PUT":
                authenticated_data = json.loads(auth_response.content.decode('utf-8'))
                request_data = json.loads(request.body.decode('utf-8'))

                if not authenticated_data['id'] == request_data['creator_user_id']:
                    return JsonResponse({'Error': 'Unauthorized to create tags'}, status=HTTP_403_FORBIDDEN)

        return self.get_response(request)
