import pytest
from urllib.parse import urlencode

from faker import Faker
from rest_framework.test import APIRequestFactory, APIClient
from django.test import override_settings, modify_settings


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def debug_mode_off():
    with override_settings(DEBUG=False):
        yield


@pytest.fixture
def remove_auth():
    with modify_settings(MIDDLEWARE={
        "remove": 'backend.middleware.auth.AuthMiddleware'
    }):
        yield


@pytest.fixture
def request_builder():
    def _request_builder(method, path, data=None, query_params=None, meta=None, format_="json"):
        request = getattr(APIRequestFactory(), method.lower())(
            path,
            data=data,
            QUERY_STRING=urlencode(query_params, True) if query_params else None,
            format=format_,
        )

        # Reconcile Django vs DRF differences
        request.query_params = request.GET
        request.data = data

        if meta:
            request.META.update(meta)

        return request
    return _request_builder


@pytest.fixture
def fake():
    return Faker()
