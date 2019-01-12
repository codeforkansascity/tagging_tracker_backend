from rest_framework import status

from backend.controllers.index import index


def test_index_returns_status():
    request = {}
    response = index(request)
    assert response.data == {"status": "running"}
    assert response.status_code == status.HTTP_200_OK
