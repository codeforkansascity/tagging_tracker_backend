import json

import pytest
from django.contrib.gis.geos import Point
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from backend.models import Address, Tag, PropertyType

pytestmark = pytest.mark.usefixtures("db")


def test_get_address_exists_returned(client, address_builder):
    address = address_builder()

    response = client.get(reverse("address", kwargs={"pk": address.id}))
    assert response.status_code == status.HTTP_200_OK, response.data


def test_delete_address(client, address_builder):
    address = address_builder()

    response = client.delete(reverse("address", kwargs={"pk": address.id}))
    assert response.status_code == status.HTTP_200_OK
    assert Address.objects.filter(pk=address.id).exists() is False


def test_create_address(client, fake, property_type_builder):
    pt = property_type_builder()

    data = {
        "neighborhood": "Some neighborhood",
        "street": fake.street_address(),
        "city": fake.city(),
        "state": fake.state(),
        "zip": fake.zipcode(),
        "creator_user_id": "some id",
        "last_updated_user_id": "some other id",
        "point": "POINT(1 1)",
        "property_type": pt.id,
    }

    response = client.post(
        reverse("address-list"), data=json.dumps(data), content_type="application/json"
    )

    assert response.status_code == status.HTTP_201_CREATED

    response_data = json.loads(response.content)
    observed_data = response_data["properties"]
    assert observed_data["neighborhood"] == data["neighborhood"]
    assert observed_data["street"] == data["street"]


def test_get_address_tags(client, tag_builder):
    tag_one = tag_builder()
    address = tag_one.address

    tag_two = tag_builder(address=address)

    response = client.get(reverse("address-tags", kwargs={"pk": address.id}))

    assert response.status_code == status.HTTP_200_OK

    response_data = json.loads(response.content)
    assert [tag_one.id, tag_two.id] == sorted([t["id"] for t in response_data])


def test_list_addresses(client, address_builder):

    address_one = address_builder()
    address_two = address_builder(property_type=address_one.property_type)

    response = client.get(reverse("address-list"))

    assert response.status_code == status.HTTP_200_OK

    response_data = json.loads(response.content)
    observed_data = response_data["features"]
    assert [address_one.id, address_two.id] == sorted([a["id"] for a in observed_data])


def test_property_types_returned(client, property_type_builder):
    pt = property_type_builder()

    response = client.get(reverse("property-types"))

    assert response.status_code == status.HTTP_200_OK
    assert response.data.pop()["id"] == pt.id
