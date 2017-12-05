from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from backend.models import Address, Tag
from backend.serializers import AddressSerializer, TagSerializer

@csrf_exempt
def address_list(request):
    """
    List all addresses or create a new one.
    :param request:
    :return: list of addresses
    """
    if request.method == "GET":
        addresses = Address.objects.all()
        serializer = AddressSerializer(addresses, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = AddressSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def tag_list(request):
    """
    List all tags or create a new one.
    :param request:
    :return: list of tags
    """
    if request.method == "GET":
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = TagSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def tag_detail(request, pk):
    """
    Retrieve, update or delete a tag
    :param request:
    :param pk:
    :return: details of a tag
    """
    try:
        tag = Tag.objects.get(pk=pk)
    except Tag.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TagSerializer(tag)
        return JsonResponse(serializer.data)

    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = TagSerializer(tag, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        tag.delete()
        return HttpResponse(status=204)