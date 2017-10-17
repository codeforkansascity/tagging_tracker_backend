from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from backend.models import TaggingPoint
from backend.serializers import TaggingPointSerializer


@csrf_exempt
def taggingpoint_list(request):
    """
    List all tagging points or create a new one.
    :param request:
    :return: yo mama
    """
    if request.method == "GET":
        taggingpoints = TaggingPoint.objects.all()
        serializer = TaggingPointSerializer(taggingpoints, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = TaggingPointSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def taggingpoint_detail(request, pk):
    """
    Retrieve, update or delete a tagging point
    :param request:
    :param pk:
    :return: also yo mama
    """
    try:
        taggingpoint = TaggingPoint.objects.get(pk=pk)
    except TaggingPoint.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TaggingPointSerializer(taggingpoint)
        return JsonResponse(serializer.data)

    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = TaggingPointSerializer(taggingpoint, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        taggingpoint.delete()
        return HttpResponse(status=204)