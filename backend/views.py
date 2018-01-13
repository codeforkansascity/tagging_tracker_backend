import urllib3
import json
import csv

from djqscsv import render_to_csv_response

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework_auth0.decorators import token_required, is_authenticated
from rest_framework_auth0.authentication import Auth0JSONWebTokenAuthentication
from backend.models import Address, Tag
from backend.serializers import AddressSerializer, TagSerializer


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


@csrf_exempt
def index(request):
    return HttpResponse(status=204)


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
        authentication_request = get_authenticated_user(request)

        if not authentication_request.status_code == 200:
            return authentication_request

        authenticated_data = json.loads(authentication_request.content.decode('utf-8'))
        request_data = json.loads(request.body.decode('utf-8'))

        if not authenticated_data['id'] == request_data['creator_user_id']:
            return JsonResponse({"Error": authenticated_data["id"] + " " + request_data['creator_user_id']}, status=403)

        data = JSONParser().parse(request)
        serializer = AddressSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def address_detail(request, pk):
    """
    Retrieve, update or delete a tag
    :param request:
    :param pk:
    :return: details of a tag
    """
    try:
        address = Address.objects.get(pk=pk)
    except Address.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = AddressSerializer(address)
        return JsonResponse(serializer.data)

    elif request.method == 'DELETE':
        authentication_request = get_authenticated_user(request)

        if not authentication_request.status_code == 200:
            return authentication_request

        address.delete();
        return HttpResponse(status=204)


@csrf_exempt
def address_tags(request, pk):
    """
    Retrieve, update or delete a tag
    :param request:
    :param pk:
    :return: details of a tag
    """
    try:
        address = Address.objects.get(pk=pk)
    except Address.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return JsonResponse(serializer.data, safe=False)


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
        authentication_request = get_authenticated_user(request)

        if not authentication_request.status_code == 200:
            return authentication_request

        authenticated_data = json.loads(authentication_request.content.decode('utf-8'))
        request_data = json.loads(request.body.decode('utf-8'))

        if not authenticated_data['id'] == request_data['creator_user_id']:
            return JsonResponse({'Error': 'Unauthorized to create tags'}, status=403)

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
        authentication_request = get_authenticated_user(request)

        if not authentication_request.status_code == 200:
            return authentication_request

        authenticated_data = json.loads(authentication_request.content.decode('utf-8'))
        request_data = json.loads(request.body.decode('utf-8'))

        if not authenticated_data['id'] == request_data['last_updated_user_id']:
            return JsonResponse({'Error': 'Unauthorized to update tag'}, status=403)

        data = JSONParser().parse(request)
        serializer = TagSerializer(tag, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        authentication_request = get_authenticated_user(request)

        if not authentication_request.status_code == 200:
            return authentication_request

        tag.delete()
        return HttpResponse(status=204)


@csrf_exempt
def csv_address_export(request):
    """
    Allows for the download of the database as a .csv file
    :param request:
    :return: a .csv file for download
    """
    if request.method == "GET":
        addresses = Address.objects.all()
        return render_to_csv_response(queryset=addresses, filename='addresses.csv', append_datestamp=True)
