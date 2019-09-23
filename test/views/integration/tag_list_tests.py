import json

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from backend.models import Tag

pytestmark = pytest.mark.usefixtures("db")


def test_get_returns_list_of_tags(client, tag_builder):
    tag_one = tag_builder()

    tag_two = tag_builder(address=tag_one.address)

    response = client.get(reverse("tag-list"))
    assert response.status_code == status.HTTP_200_OK
    assert [tag_one.id, tag_two.id] == sorted(
        [t["id"] for t in json.loads(response.content)]
    )


def test_post_request_creates_tag(client, fake, address_builder):
    address = address_builder()

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
