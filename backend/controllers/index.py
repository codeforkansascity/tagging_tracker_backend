from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response


@csrf_exempt
def index(request):
    return Response({"status": "running"}, status=status.HTTP_200_OK)
