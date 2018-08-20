import json
import os
import urllib3

from django.http import JsonResponse

from backend.controllers.controller_utils import HTTP_STATUS_OK, HTTP_STATUS_UNAUTHORIZED, HTTP_STATUS_FORBIDDEN,\
    HTTP_STATUS_INTERNAL_SERVER_ERROR


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST" or request.method == "DELETE" or request.method == "PUT":
            auth = request.META.get("HTTP_AUTHORIZATION", None)

            if not auth or len(auth.split()) != 2:
                return JsonResponse({"Error": "Unauthenticated"}, status=HTTP_STATUS_UNAUTHORIZED)

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

            if not auth_response.status == HTTP_STATUS_OK:
                if auth_response.status == HTTP_STATUS_FORBIDDEN or auth_response.status == HTTP_STATUS_UNAUTHORIZED:
                    return JsonResponse({"Error": "Unauthorized"}, status=HTTP_STATUS_UNAUTHORIZED)
                else:
                    return JsonResponse({"Error": "Internal Server Error"}, status=HTTP_STATUS_INTERNAL_SERVER_ERROR)

            if request.method == "POST" or request.method == "PUT":
                authenticated_data = json.loads(auth_response.content.decode('utf-8'))
                request_data = json.loads(request.body.decode('utf-8'))

                if not authenticated_data['id'] == request_data['creator_user_id']:
                    return JsonResponse({'Error': 'Unauthorized to create tags'}, status=HTTP_STATUS_FORBIDDEN)

        return self.get_response(request)
