import json
import logging
import os

import requests
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from auth.validators import TokenValidator

logger = logging.getLogger(__name__)


@api_view(["POST"])
def get_token(request):

    validator = TokenValidator(data=request.data)
    if not validator.is_valid():
        return Response(validator.errors, status=status.HTTP_400_BAD_REQUEST)

    data = {
        "grant_type": "password",
        "username": validator.validated_data["username"],
        "password": validator.validated_data["password"],
        "audience": os.environ["AUTH0_AUDIENCE"],
        "client_id": os.environ["AUTH0_CLIENTID"],
        "client_secret": os.environ["AUTH0_SECRET"]
    }

    response = requests.post(
        "https://" + os.environ["AUTH0_URL"] + "/oauth/token",
        data=json.dumps(data).encode("utf8"),
        headers={"content-type": "application/json"}
    )

    data = response.json()

    if response.status_code != status.HTTP_200_OK:
        if response.status_code == status.HTTP_403_FORBIDDEN:
            return Response(data, status=status.HTTP_403_FORBIDDEN)
        logger.debug(f"Invalid token generation: status {response.status_code} data {data}")
        return HttpResponseServerError()

    return Response(data)
