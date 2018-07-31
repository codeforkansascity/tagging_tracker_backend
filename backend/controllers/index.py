from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from backend.controllers.controller_utils import HTTP_STATUS_NO_CONTENT

@csrf_exempt
def index(request):
    return HttpResponse(status=HTTP_STATUS_NO_CONTENT)
