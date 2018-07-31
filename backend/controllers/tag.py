from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from backend.models import Tag
from backend.serializers import TagSerializer

from backend.controllers.controller_utils import HTTP_STATUS_CREATED, HTTP_STATUS_NO_CONTENT, HTTP_STATUS_BAD_REQUEST,\
    HTTP_STATUS_NOT_FOUND, HTTP_STATUS_METHOD_NOT_ALLOWED


class TagResource:

    @csrf_exempt
    def tag_detail(self, request, pk):
        """
        Retrieve, update or delete a tag
        :param request:
        :param pk:
        :return: details of a tag
        """
        try:
            tag = Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            return HttpResponse(status=HTTP_STATUS_NOT_FOUND)

        response = HttpResponse(status=HTTP_STATUS_METHOD_NOT_ALLOWED)
        if request.method == 'GET':
            response = self.__retrieve_tag_detail(tag)
        elif request.method == "PUT":
            response = self.__update_tag_detail(request, tag)
        elif request.method == 'DELETE':
            response = self.__delete_tag_detail(tag)

        return response

    @csrf_exempt
    def tag_list(self, request):
        """
        List all tags or create a new one.
        :param request:
        :return: list of tags
        """
        response = HttpResponse(status=HTTP_STATUS_METHOD_NOT_ALLOWED)
        if request.method == "GET":
            response = self.__list_tags()
        elif request.method == "POST":
            response = self.__create_tag(request)
        return response

    def __retrieve_tag_detail(self, tag):
        serializer = TagSerializer(tag)
        return JsonResponse(serializer.data)

    def __update_tag_detail(self, request, tag):
        data = JSONParser().parse(request)
        serializer = TagSerializer(tag, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=HTTP_STATUS_BAD_REQUEST)

    def __delete_tag_detail(self, tag):
        tag.delete()
        return HttpResponse(status=HTTP_STATUS_NO_CONTENT)

    def __list_tags(self):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return JsonResponse(serializer.data, safe=False)

    def __create_tag(self, request):
        data = JSONParser().parse(request)
        serializer = TagSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=HTTP_STATUS_CREATED)
        return JsonResponse(serializer.errors, status=HTTP_STATUS_BAD_REQUEST)
