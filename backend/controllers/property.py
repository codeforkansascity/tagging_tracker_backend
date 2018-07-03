from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from backend.controllers.controller_utils import HTTP_STATUS_METHOD_NOT_ALLOWED, HTTP_STATUS_CREATED, \
    HTTP_STATUS_BAD_REQUEST
from backend.models import PropertyType
from backend.serializers import PropertyTypeSerializer


@csrf_exempt
def property_type_list(request):
    """
    List all property types or create a new one.
    :param request:
    :return: list of property types
    """
    response = HttpResponse(status=HTTP_STATUS_METHOD_NOT_ALLOWED)
    if request.method == "GET":
        response = __retrieve_property_types()
    elif request.method == "POST":
        response = __create_property_type(request)
    return response


def __retrieve_property_types():
    property_types = PropertyType.objects.all()
    serializer = PropertyTypeSerializer(property_types, many=True)
    return JsonResponse(data=serializer.data, safe=False)


def __create_property_type(request):
    data = JSONParser().parse(request)
    serializer = PropertyTypeSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=HTTP_STATUS_CREATED)
    return JsonResponse(serializer.errors, status=HTTP_STATUS_BAD_REQUEST)
