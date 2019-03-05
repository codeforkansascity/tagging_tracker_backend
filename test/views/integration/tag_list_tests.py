import json

import pytest
from django.contrib.gis.geos import Point
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from backend.models import Address, Tag, PropertyType

pytestmark = pytest.mark.usefixtures("db")


def test_get_returns_list_of_tags(client, fake):
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

    response = client.get(reverse("tag-list"))
    assert response.status_code == status.HTTP_200_OK
    assert [tag_one.id, tag_two.id] == sorted(
        [t["id"] for t in json.loads(response.content)]
    )


def test_post_request_creates_tag(client, fake):
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

    data = {
        "address": address.id,
        "creator_user_id": "some id",
        "last_updated_user_id": "some id",
        "description": fake.text(),
        "date_taken": timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    response = client.post(
        reverse("tag-list"), json.dumps(data), content_type="application/json"
    )
    assert response.status_code == status.HTTP_201_CREATED, response.content
    assert Tag.objects.filter(description=data["description"]).exists() is True
