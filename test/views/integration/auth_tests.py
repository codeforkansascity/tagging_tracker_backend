import os

import pytest
import requests
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.usefixtures("enable_auth")


def test_get_token_works_with_valid_user(live_server):

    data = {
        "username": os.environ["AUTH0_TEST_USER"],
        "password": os.environ["AUTH0_TEST_PASS"]
    }
    response = requests.post(live_server + reverse("token"), data)
    assert response.status_code == status.HTTP_200_OK, response.content
