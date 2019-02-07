import pytest
from rest_framework import status
from rest_framework.views import APIView

from common.auth import jwt_get_username_from_payload_handler, get_token_auth_header, has_valid_scope

pytestmark = pytest.mark.unit


def test_jwt_get_username_from_payload_handler(mocker):
    auth_mock = mocker.patch("common.auth.authenticate")

    payload = {
        "sub": "auth|d41d8cd98f00b204e9800998ecf8427e"
    }

    username = jwt_get_username_from_payload_handler(payload)
    assert username == "auth.d41d8cd98f00b204e9800998ecf8427e"
    auth_mock.assert_called_once_with(remote_user=username)


def test_get_token_auth_header_gets_token(request_builder):
    token = "mytoken"
    request = request_builder("GET", "/some/endpoint")
    request.META = {
        "HTTP_AUTHORIZATION": "Bearer " + token
    }

    assert get_token_auth_header(request) == token


def test_has_valid_scope_returns_true_if_valid_scope(mocker, request_builder):
    scope = "read:write"
    payload = {
        "scope": scope
    }

    jwt_decode = mocker.patch("common.auth.jwt.decode")
    jwt_decode.return_value = payload

    request = request_builder("GET", "/some/endpoint")
    request.META = {
        "HTTP_AUTHORIZATION": "Bearer token"
    }

    assert has_valid_scope(request, scope) is True


def test_has_valid_scope_returns_false_if_invalid_scope(mocker, request_builder):
    scope = "read:write"
    payload = {
        "scope": "another:scope"
    }

    jwt_decode = mocker.patch("common.auth.jwt.decode")
    jwt_decode.return_value = payload

    request = request_builder("GET", "/some/endpoint")
    request.META = {
        "HTTP_AUTHORIZATION": "Bearer token"
    }

    assert has_valid_scope(request, scope) is False


def test_has_valid_scope_returns_false_if_scope_not_found(mocker, request_builder):
    scope = "read:write"
    payload = {}

    jwt_decode = mocker.patch("common.auth.jwt.decode")
    jwt_decode.return_value = payload

    request = request_builder("GET", "/some/endpoint")
    request.META = {
        "HTTP_AUTHORIZATION": "Bearer token"
    }

    assert has_valid_scope(request, scope) is False
