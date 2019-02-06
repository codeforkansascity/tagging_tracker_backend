from rest_framework import status

from auth.views import get_token


def test_invalid_parameters_response_structure(mocker, request_builder):
    is_valid = mocker.patch("auth.views.TokenValidator.is_valid")
    is_valid.return_value = False

    errors = mocker.patch("auth.views.TokenValidator.errors", new_callable=mocker.PropertyMock)
    expected_errors = {}
    errors.return_value = expected_errors

    request = request_builder("POST", "blah")

    response = get_token(request)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == expected_errors


def test_auth0_returns_403_response_structure(mocker, request_builder):
    req_pack = mocker.patch("auth.views.requests")
    mock_response = req_pack.post.return_value
    mock_response.status_code = status.HTTP_403_FORBIDDEN

    data = {
        "username": "someone@example.com",
        "password": "somepass"
    }

    request = request_builder("POST", "/some/endpoint", data)

    response = get_token(request)

    assert response.status_code == status.HTTP_403_FORBIDDEN, response.data
    assert response.data == mock_response.json.return_value


def test_auth0_returns_unhandled_status_response_structure(mocker, request_builder):
    req_pack = mocker.patch("auth.views.requests")
    mock_response = req_pack.post.return_value
    mock_response.status_code = status.HTTP_302_FOUND

    data = {
        "username": "someone@example.com",
        "password": "somepass"
    }

    request = request_builder("POST", "/some/endpoint", data)

    response = get_token(request)

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR, response.data
    assert response.content == b""


def test_valid_parameters_response_structure(mocker, request_builder):
    req_pack = mocker.patch("auth.views.requests")
    mock_response = req_pack.post.return_value
    mock_response.status_code = status.HTTP_200_OK

    data = {
        "username": "someone@example.com",
        "password": "somepass"
    }

    request = request_builder("POST", "/some/endpoint", data)

    response = get_token(request)

    assert response.status_code == status.HTTP_200_OK, response.data
    assert response.data == mock_response.json.return_value
