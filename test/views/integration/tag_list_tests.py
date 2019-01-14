import json
from datetime import datetime

import pytest
from django.contrib.gis.geos import Point
from django.urls import reverse
from rest_framework import status

from backend.models import Address, Tag

pytestmark = pytest.mark.usefixtures("db")


def test_get_returns_list_of_tags(client, fake):
    address = Address(
        point=Point(1, 2),
        neighborhood="Some neighborhood",
        street=fake.street_address(),
        city=fake.city(),
        state=fake.state(),
        zip=fake.zipcode(),
        creator_user_id="some id",
        last_updated_user_id="some id",
        owner_name=fake.first_name(),
        owner_email=fake.safe_email(),
        tenant_name=fake.name(),
        tenant_email=fake.safe_email(),
        follow_up_owner_needed=True,
        land_bank_property=True,
        type_of_property=1
    )
    address.save()
    address.refresh_from_db()

    tag_one = Tag(
        address=address,
        creator_user_id="some id",
        last_updated_user_id="some id",
        date_taken=datetime.utcnow(),
        description=fake.text(),
    )
    tag_one.save()
    tag_one.refresh_from_db()

    tag_two = Tag(
        address=address,
        creator_user_id="some id",
        last_updated_user_id="some id",
        date_taken=datetime.utcnow(),
        description=fake.text(),
    )
    tag_two.save()
    tag_two.refresh_from_db()

    response = client.get(reverse("tag_list"))
    assert response.status_code == status.HTTP_200_OK
    assert [tag_one.id, tag_two.id] == sorted([t["id"] for t in json.loads(response.content)])


def test_post_request_creates_tag(client, fake):
    address = Address(
        point=Point(1, 2),
        neighborhood="Some neighborhood",
        street=fake.street_address(),
        city=fake.city(),
        state=fake.state(),
        zip=fake.zipcode(),
        creator_user_id="some id",
        last_updated_user_id="some id",
        owner_name=fake.first_name(),
        owner_email=fake.safe_email(),
        tenant_name=fake.name(),
        tenant_email=fake.safe_email(),
        follow_up_owner_needed=True,
        land_bank_property=True,
        type_of_property=1
    )
    address.save()
    address.refresh_from_db()

    data = {
        "address": address.id,
        "creator_user_id": "some id",
        "last_updated_user_id": "some id",
        "description": fake.text(),
        "date_taken": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
    }

    response = client.post(reverse("tag_list"), json.dumps(data), content_type="application/json")
    assert response.status_code == status.HTTP_201_CREATED, response.content
    assert Tag.objects.filter(description=data["description"]).exists() is True
