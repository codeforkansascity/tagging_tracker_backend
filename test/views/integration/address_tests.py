import json

import pytest
from django.contrib.gis.geos import Point
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from backend.models import Address, Tag, PropertyType

pytestmark = pytest.mark.usefixtures("db")


def test_get_address_exists_returned(client, fake):
    pt = PropertyType(slug="some_slug")
    pt.save()
    pt.refresh_from_db()

    address = Address(
        point=Point(1, 2),
        neighborhood="Some neighborhood",
        street=fake.street_address(),
        city=fake.city(),
        state=fake.state(),
        zip=fake.zipcode(),
        creator_user_id="some id",
        last_updated_user_id="some id",
        land_bank_property=True,
        property_type=pt
    )
    address.save()
    address.refresh_from_db()

    response = client.get(reverse("address", kwargs={"pk": address.id}))
    assert response.status_code == status.HTTP_200_OK, response.data


def test_delete_address(client, fake):
    pt = PropertyType(slug="some_slug")
    pt.save()
    pt.refresh_from_db()

    address = Address(
        point=Point(1, 2),
        neighborhood="Some neighborhood",
        street=fake.street_address(),
        city=fake.city(),
        state=fake.state(),
        zip=fake.zipcode(),
        creator_user_id="some id",
        last_updated_user_id="some id",
        land_bank_property=True,
        property_type=pt
    )
    address.save()
    address.refresh_from_db()

    response = client.delete(reverse("address", kwargs={"pk": address.id}))
    assert response.status_code == status.HTTP_200_OK
    assert Address.objects.filter(pk=address.id).exists() is False


def test_create_address(client, fake):
    pt = PropertyType(slug="some_slug")
    pt.save()
    pt.refresh_from_db()

    data = {
        "neighborhood": "Some neighborhood",
        "street": fake.street_address(),
        "city": fake.city(),
        "state": fake.state(),
        "zip": fake.zipcode(),
        "creator_user_id": "some id",
        "last_updated_user_id": "some other id",
        "point": "POINT(1 1)",
        "property_type": pt.id
    }

    response = client.post(reverse("address-list"), data=json.dumps(data), content_type="application/json")

    assert response.status_code == status.HTTP_201_CREATED

    response_data = json.loads(response.content)
    observed_data = response_data["properties"]
    assert observed_data["neighborhood"] == data["neighborhood"]
    assert observed_data["street"] == data["street"]


def test_get_address_tags(client, fake):
    pt = PropertyType(slug="some_slug")
    pt.save()
    pt.refresh_from_db()

    address = Address(
        point=Point(1, 2),
        neighborhood="Some neighborhood",
        street=fake.street_address(),
        city=fake.city(),
        state=fake.state(),
        zip=fake.zipcode(),
        creator_user_id="some id",
        last_updated_user_id="some id",
        land_bank_property=True,
        property_type=pt
    )
    address.save()
    address.refresh_from_db()

    tag_one = Tag(
        address=address,
        creator_user_id="some id",
        last_updated_user_id="some id",
        date_taken=timezone.now(),
        description=fake.text(),
    )
    tag_one.save()
    tag_one.refresh_from_db()

    tag_two = Tag(
        address=address,
        creator_user_id="some id",
        last_updated_user_id="some id",
        date_taken=timezone.now(),
        description=fake.text(),
    )
    tag_two.save()
    tag_two.refresh_from_db()

    response = client.get(reverse("address-tags", kwargs={"pk": address.id}))

    assert response.status_code == status.HTTP_200_OK

    response_data = json.loads(response.content)
    assert [tag_one.id, tag_two.id] == sorted([t["id"] for t in response_data])


def test_list_addresses(client, fake):
    pt = PropertyType(slug="some_slug")
    pt.save()
    pt.refresh_from_db()

    address_one = Address(
        point=Point(1, 2),
        neighborhood="Some neighborhood",
        street=fake.street_address(),
        city=fake.city(),
        state=fake.state(),
        zip=fake.zipcode(),
        creator_user_id="some id",
        last_updated_user_id="some id",
        land_bank_property=True,
        property_type=pt
    )
    address_one.save()
    address_one.refresh_from_db()

    address_two = Address(
        point=Point(1, 2),
        neighborhood="Some neighborhood",
        street=fake.street_address(),
        city=fake.city(),
        state=fake.state(),
        zip=fake.zipcode(),
        creator_user_id="some id",
        last_updated_user_id="some id",
        land_bank_property=True,
        property_type=pt
    )
    address_two.save()
    address_two.refresh_from_db()

    response = client.get(reverse("address-list"))

    assert response.status_code == status.HTTP_200_OK

    response_data = json.loads(response.content)
    observed_data = response_data["features"]
    assert [address_one.id, address_two.id] == sorted([a["id"] for a in observed_data])


def test_property_types_returned(client):
    pt = PropertyType(slug="some_slug")
    pt.save()
    pt.refresh_from_db()

    response = client.get(reverse("property-types"))

    assert response.status_code == status.HTTP_200_OK
    assert response.data.pop()["id"] == pt.id
