from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_405_METHOD_NOT_ALLOWED

from backend.models import Address, Tag
from backend.serializers import TagSerializer


@csrf_exempt
def address_tags(request, pk):
    """
    Retrieve an address' tags
    :param request:
    :param pk:
    :return: details of tags
    """
    try:
        address = Address.objects.get(pk=pk)
    except Address.DoesNotExist:
        return HttpResponse(status=HTTP_404_NOT_FOUND)

    response = HttpResponse(status=HTTP_405_METHOD_NOT_ALLOWED)
    if request.method == 'GET':
        response = __retrieve_tags_by_address(address)

    return response


def __retrieve_tags_by_address(address):
    tags = Tag.objects.filter(address=address)
    serializer = TagSerializer(tags, many=True)
    return JsonResponse(serializer.data, safe=False)
