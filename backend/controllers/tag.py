import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from backend.models import Tag
from backend.serializers import TagSerializer

from backend.controllers.view_utils import get_authenticated_user


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

    response = HttpResponse(status=405)
    if request.method == 'GET':
        response = __retrieve_tag_detail(tag)
    elif request.method == "PUT":
        response = __update_tag_detail(request, tag)
    elif request.method == 'DELETE':
        response = __delete_tag_detail(request, tag)

    return response


@csrf_exempt
def tag_list(request):
    """
    List all tags or create a new one.
    :param request:
    :return: list of tags
    """
    response = HttpResponse(status=405)
    if request.method == "GET":
        response = __list_tags()
    elif request.method == "POST":
        response = __create_tag(request)
    return response


def __retrieve_tag_detail(tag):
    serializer = TagSerializer(tag)
    return JsonResponse(serializer.data)


def __update_tag_detail(request, tag):
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


def __delete_tag_detail(request, tag):
    authentication_request = get_authenticated_user(request)

    if not authentication_request.status_code == 200:
        return authentication_request

    tag.delete()
    return HttpResponse(status=204)


def __list_tags():
    tags = Tag.objects.all()
    serializer = TagSerializer(tags, many=True)
    return JsonResponse(serializer.data, safe=False)


def __create_tag(request):
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
