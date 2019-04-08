from rest_framework import status

from backend.views.index import index


def test_index_returns_status(request_builder):
    request = request_builder("GET", "/")
    response = index(request)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {"status": "running"}
