import json

import pytest
from django.contrib.gis.geos import Point
from django.urls import reverse
from rest_framework import status

from backend.models import Contact, ContactType, Address, PropertyType

pytestmark = pytest.mark.usefixtures("db")


def test_contact_list_returns_valid(client, contact_builder):

    contact = contact_builder()

    response = client.get(
        reverse("address-contacts", kwargs={"pk": contact.address.id})
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data.pop()["id"] == contact.id


def test_create_contact_returns_valid(
    client, fake, contact_type_builder, address_builder
):
    address = address_builder()

    ct = contact_type_builder()

    data = {
        "address": address.id,
        "contact_type": ct.id,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
    }

    response = client.post(
        reverse("address-contacts", kwargs={"pk": address.id}),
        json.dumps(data),
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["email"] == data["email"]


def test_update_contact_returns_valid(client, fake, contact_builder):

    contact = contact_builder()

    data = {
        "address": contact.address.id,
        "contact_type": contact.contact_type.id,
        "first_name": fake.first_name(),
        "last_name": contact.last_name,
        "email": contact.email,
        "phone": contact.phone,
    }

    response = client.put(
        reverse("contact", kwargs={"address_pk": data["address"], "pk": contact.id}),
        json.dumps(data),
        content_type="application/json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["first_name"] == data["first_name"]


def test_contact_view_delete(client, contact_builder):
    contact = contact_builder()

    response = client.delete(
        reverse("contact", kwargs={"address_pk": contact.address.id, "pk": contact.id})
    )
    assert response.status_code == status.HTTP_200_OK
    assert Contact.objects.filter(pk=contact.id).exists() is False


def test_contact_types_returns_list_of_contact_types(client, contact_type_builder):
    _ = contact_type_builder(slug="some-slug")

    _ = contact_type_builder(slug="some-slug2")

    response = client.get(reverse("contact-types"))
    assert response.status_code == status.HTTP_200_OK
    assert sorted(["some-slug", "some-slug2"]) == sorted(
        [d["slug"] for d in response.data]
    )


def test_contact_view_returns_valid_contact(client, contact_builder):
    contact = contact_builder()

    response = client.get(
        reverse("contact", kwargs={"address_pk": contact.address.id, "pk": contact.id})
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == contact.id
