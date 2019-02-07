import pytest
from rest_framework import status
from rest_framework.views import APIView

from common.auth import jwt_get_username_from_payload_handler, get_token_auth_header, requires_scope

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


@pytest.mark.usefixtures("enable_auth")
def test_requires_scope_valid_scope_returns_function_call(mocker, request_builder):
    scope = "read:write"
    payload = {
        "scope": scope
    }

    jwt_decode = mocker.patch("common.auth.jwt.decode")
    jwt_decode.return_value = payload

    @requires_scope(scope)
    def view_func(*args, **kwargs):
        return "Hello"

    request = request_builder("GET", "/some/endpoint")
    request.META = {
        "HTTP_AUTHORIZATION": "Bearer token"
    }

    response = view_func(request)
    assert response == "Hello"
    jwt_decode.assert_called_once()


@pytest.mark.usefixtures("enable_auth")
def test_requires_scope_valid_scope_returns_class_method_call(mocker, request_builder):
    scope = "read:write"
    payload = {
        "scope": scope
    }

    jwt_decode = mocker.patch("common.auth.jwt.decode")
    jwt_decode.return_value = payload

    class MyView(APIView):

        @requires_scope(scope)
        def get(self, request):
            return "Hello"

    request = request_builder("GET", "/some/endpoint")
    request.META = {
        "HTTP_AUTHORIZATION": "Bearer token"
    }

    response = MyView().get(request)
    assert response == "Hello"
    jwt_decode.assert_called_once()


@pytest.mark.usefixtures("enable_auth")
def test_requires_scope_invalid_scope_returns_403(mocker, request_builder):
    scope = "read:write"
    payload = {
        "scope": scope
    }

    jwt_decode = mocker.patch("common.auth.jwt.decode")
    jwt_decode.return_value = payload

    @requires_scope("hello")
    def view_func(*args, **kwargs):
        return "Hello"

    request = request_builder("GET", "/some/endpoint")
    request.META = {
        "HTTP_AUTHORIZATION": "Bearer token"
    }

    response = view_func(request)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.data == {"message": "You do not have access to this resource"}
