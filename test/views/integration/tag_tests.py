import json

import pytest
from django.urls import reverse
from rest_framework import status

from backend.models import Tag

pytestmark = pytest.mark.usefixtures("db")


def test_get_method_retrieves_existing_tag(client, tag_builder):
    tag = tag_builder()

    response = client.get(reverse("tag", kwargs={"pk": tag.id}))
    assert response.status_code == status.HTTP_200_OK
    assert json.loads(response.content)["id"] == tag.id


def test_put_method_updates_tag(client, tag_builder):
    tag = tag_builder()

    updated = {
        "address": tag.address.id,
        "creator_user_id": tag.creator_user_id,
        "last_updated_user_id": tag.last_updated_user_id,
        "date_taken": tag.date_taken.strftime("%Y-%m-%d %H:%M:%S"),
        "description": "new subscription",
    }

    response = client.put(
        reverse("tag", kwargs={"pk": tag.id}),
        json.dumps(updated),
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_200_OK, response.content
    tag.refresh_from_db()
    assert tag.description == updated["description"]


def test_deleted_method_deletes_tag(client, tag_builder):
    tag = tag_builder()

    response = client.delete(reverse("tag", kwargs={"pk": tag.id}))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Tag.objects.filter(pk=tag.id).exists() is False
