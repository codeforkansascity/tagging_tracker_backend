import json

import pytest
from django.contrib.gis.geos import Point
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from backend.models import Address, Tag

pytestmark = pytest.mark.usefixtures("db")


def test_get_method_retrieves_existing_tag(client, fake):
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
        type_of_property=1
    )
    address.save()
    address.refresh_from_db()

    tag = Tag(
        address=address,
        creator_user_id="some id",
        last_updated_user_id="some id",
        date_taken=timezone.now(),
        description="some description",
        img="something goes here",
        square_footage="some sq ft",
        surface="concrete",
        tag_words="some words",
        tag_initials="someones initial"
    )
    tag.save()
    tag.refresh_from_db()

    response = client.get(reverse("tag", kwargs={"pk": tag.id}))
    assert response.status_code == status.HTTP_200_OK
    assert json.loads(response.content)["id"] == tag.id


def test_put_method_updates_tag(client, fake):
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
        type_of_property=1
    )
    address.save()
    address.refresh_from_db()

    tag = Tag(
        address=address,
        creator_user_id="some id",
        last_updated_user_id="some id",
        date_taken=timezone.now(),
        description="some description",
        img="something goes here",
        square_footage="some sq ft",
        surface="concrete",
        tag_words="some words",
        tag_initials="someones initial"
    )
    tag.save()
    tag.refresh_from_db()

    updated = {
        "address": address.id,
        "creator_user_id": tag.creator_user_id,
        "last_updated_user_id": tag.last_updated_user_id,
        "date_taken": tag.date_taken.strftime("%Y-%m-%d %H:%M:%S"),
        "description": "new subscription"
    }

    response = client.put(reverse("tag", kwargs={"pk": tag.id}), json.dumps(updated), content_type="application/json")
    assert response.status_code == status.HTTP_200_OK, response.content
    tag.refresh_from_db()
    assert tag.description == updated["description"]


def test_deleted_method_deletes_tag(client, fake):
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
        type_of_property=1
    )
    address.save()
    address.refresh_from_db()

    tag = Tag(
        address=address,
        creator_user_id="some id",
        last_updated_user_id="some id",
        date_taken=timezone.now(),
        description="some description",
        img="something goes here",
        square_footage="some sq ft",
        surface="concrete",
        tag_words="some words",
        tag_initials="someones initial"
    )
    tag.save()
    tag.refresh_from_db()

    response = client.delete(reverse("tag", kwargs={"pk": tag.id}))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Tag.objects.filter(pk=tag.id).exists() is False
