import pytest
from django.contrib.gis.geos import Point
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from backend.models import Address, Tag, PropertyType

pytestmark = pytest.mark.usefixtures("db")


def test_export_addresses(client, fake):
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
        property_type=pt,
    )
    address.save()
    address.refresh_from_db()

    response = client.get(reverse("addresses-download"))

    assert response.status_code == status.HTTP_200_OK
    headers = response._headers
    assert headers["content-type"] == ("Content-Type", "text/csv")


def test_export_tags(client, fake):
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
        property_type=pt,
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

    response = client.get(reverse("tags-download"))

    assert response.status_code == status.HTTP_200_OK
    headers = response._headers
    assert headers["content-type"] == ("Content-Type", "text/csv")
