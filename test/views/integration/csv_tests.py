import pytest
from django.urls import reverse
from rest_framework import status


pytestmark = pytest.mark.usefixtures("db")


def test_export_addresses(client, address_builder):
    _ = address_builder()

    response = client.get(reverse("addresses-download"))

    assert response.status_code == status.HTTP_200_OK
    headers = response._headers
    assert headers["content-type"] == ("Content-Type", "text/csv")


def test_export_tags(client, tag_builder):
    tag_one = tag_builder()

    _ = tag_builder(address=tag_one.address)

    response = client.get(reverse("tags-download"))

    assert response.status_code == status.HTTP_200_OK
    headers = response._headers
    assert headers["content-type"] == ("Content-Type", "text/csv")
