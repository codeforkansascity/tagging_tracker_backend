import urllib3
import json

from django.http import JsonResponse


HTTP_STATUS_OK = 200
HTTP_STATUS_CREATED = 201
HTTP_STATUS_NO_CONTENT = 204
HTTP_STATUS_BAD_REQUEST = 400
HTTP_STATUS_FORBIDDEN = 403
HTTP_STATUS_NOT_FOUND = 404
HTTP_STATUS_METHOD_NOT_ALLOWED = 405


def get_authenticated_user(request):
    auth = request.META.get("HTTP_AUTHORIZATION", None)

    if not auth or len(auth.split()) != 2:
        return JsonResponse({"Error": "Unauthenticated"}, status=401)

    parts = auth.split()
    token = parts[1]
    http = urllib3.PoolManager()

    r = http.request(
        'GET',
        'https://taggingtrackerdev.auth0.com/userinfo',
        headers={
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json'
        }
    )

    if not r.status == 200:
        if r.status == 403 or r.status == 401:
            return JsonResponse({"Error": "Unauthorized"}, status=401)
        else:
            return JsonResponse({"Error": "Internal Server Error"}, status=500)
    else:
        return JsonResponse({"id": json.loads(r.data.decode('utf-8'))["sub"].split('|')[1]}, status=200)
