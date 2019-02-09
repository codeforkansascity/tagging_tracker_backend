import json
import pprint

import pytest
from django.contrib.gis.geos import Point
from django.urls import reverse
from rest_framework import status

from backend.models import Contact, ContactType, Address

pytestmark = pytest.mark.usefixtures("db")


def test_contact_list_returns_valid(client, fake):
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

    ct = ContactType(slug="some-slug")
    ct.save()
    ct.refresh_from_db()

    contact = Contact(
        address=address,
        contact_type=ct,
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email(),
        phone=fake.phone_number()
    )
    contact.save()
    contact.refresh_from_db()

    response = client.get(reverse("address-contacts", kwargs={"pk": address.id}))

    assert response.status_code == status.HTTP_200_OK
    assert response.data.pop()["id"] == contact.id


def test_create_contact_returns_valid(client, fake):
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

    ct = ContactType(slug="some-slug")
    ct.save()
    ct.refresh_from_db()

    data = {
        "address": address.id,
        "contact_type": ct.id,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "phone": fake.phone_number()
    }

    response = client.post(
        reverse("address-contacts", kwargs={"pk": address.id}),
        json.dumps(data),
        content_type="application/json"
    )
    pprint.pprint(response.data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["email"] == data["email"]


def test_update_contact_returns_valid(client, fake):
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

    ct = ContactType(slug="some-slug")
    ct.save()
    ct.refresh_from_db()

    contact = Contact(
        address=address,
        contact_type=ct,
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email(),
        phone=fake.phone_number()
    )
    contact.save()
    contact.refresh_from_db()

    data = {
        "id": contact.id,
        "address": address.id,
        "contact_type": ct.id,
        "first_name": fake.first_name(),
        "last_name": contact.last_name,
        "email": contact.email,
        "phone": contact.phone
    }

    response = client.put(
        reverse("address-contacts", kwargs={"pk": address.id}),
        json.dumps(data),
        content_type="application/json"
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["first_name"] == data["first_name"]


def test_contact_list_delete(client, fake):
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

    ct = ContactType(slug="some-slug")
    ct.save()
    ct.refresh_from_db()

    contact = Contact(
        address=address,
        contact_type=ct,
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email(),
        phone=fake.phone_number()
    )
    contact.save()
    contact.refresh_from_db()

    data = {
        "id": contact.id
    }

    response = client.delete(
        reverse("address-contacts", kwargs={"pk": address.id}),
        json.dumps(data),
        content_type="application/json"
    )
    assert response.status_code == status.HTTP_200_OK
    assert Contact.objects.filter(pk=data["id"]).exists() is False


def test_contact_types_returns_list_of_contact_types(client):
    ct1 = ContactType(slug="some-slug")
    ct1.save()
    ct1.refresh_from_db()

    ct1 = ContactType(slug="some-slug2")
    ct1.save()
    ct1.refresh_from_db()

    response = client.get(reverse("contact-types"))
    assert response.status_code == status.HTTP_200_OK
    assert sorted(["some-slug", "some-slug2"]) == sorted([d["slug"] for d in response.data])
