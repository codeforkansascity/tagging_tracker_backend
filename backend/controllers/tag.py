from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, \
    HTTP_405_METHOD_NOT_ALLOWED
from backend.models import Tag
from backend.serializers import TagSerializer


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
        return HttpResponse(status=HTTP_404_NOT_FOUND)

    response = HttpResponse(status=HTTP_405_METHOD_NOT_ALLOWED)
    if request.method == 'GET':
        response = __retrieve_tag_detail(tag)
    elif request.method == "PUT":
        response = __update_tag_detail(request, tag)
    elif request.method == 'DELETE':
        response = __delete_tag_detail(tag)

    return response


@csrf_exempt
def tag_list(request):
    """
    List all tags or create a new one.
    :param request:
    :return: list of tags
    """
    response = HttpResponse(status=HTTP_405_METHOD_NOT_ALLOWED)
    if request.method == "GET":
        response = __list_tags()
    elif request.method == "POST":
        response = __create_tag(request)
    return response


def __retrieve_tag_detail(tag):
    serializer = TagSerializer(tag)
    return JsonResponse(serializer.data)


def __update_tag_detail(request, tag):
    data = JSONParser().parse(request)
    serializer = TagSerializer(tag, data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data)
    return JsonResponse(serializer.errors, status=HTTP_400_BAD_REQUEST)


def __delete_tag_detail(tag):
    tag.delete()
    return HttpResponse(status=HTTP_204_NO_CONTENT)


def __list_tags():
    tags = Tag.objects.all()
    serializer = TagSerializer(tags, many=True)
    return JsonResponse(serializer.data, safe=False)


def __create_tag(request):
    data = JSONParser().parse(request)
    serializer = TagSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=HTTP_400_BAD_REQUEST)
