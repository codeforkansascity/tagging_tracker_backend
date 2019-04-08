from urllib.parse import urlencode

import pytest
from django.test import override_settings
from faker import Faker
from rest_framework.test import APIRequestFactory, APIClient


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def debug_mode_on():
    with override_settings(DEBUG=True):
        yield


@pytest.fixture
def enable_auth():
    with override_settings(DISABLE_AUTH=False):
        yield


@pytest.fixture
def request_builder():
    def _request_builder(
        method, path, data=None, query_params=None, meta=None, format_="json"
    ):
        """
        Fixture for easily building requests
        :param method: HTTP method
        :param path: request path
        :param data: request body
        :param query_params: dictionary that is encoded into query string
        :param meta: dictionary that modifies META request headers
        :param format_: api request format
        :return: django.core.handlers.wsgi.WSGIRequest
        """
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
