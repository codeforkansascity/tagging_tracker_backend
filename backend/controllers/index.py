from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework import status


@csrf_exempt
def index(request):
    return JsonResponse({"status": "running"}, status=status.HTTP_200_OK)
