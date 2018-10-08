from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.status import HTTP_204_NO_CONTENT


@csrf_exempt
def index(request):
    return HttpResponse(status=HTTP_204_NO_CONTENT)
