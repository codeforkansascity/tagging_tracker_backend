import pytest
from django.contrib.gis.geos import Point
from django.urls import reverse
from rest_framework import status

from backend.models import Address


pytestmark = pytest.mark.usefixtures("db", "remove_auth")


def test_get_address_exists_returned(client, fake):
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

    response = client.get(reverse("address", kwargs={"pk": address.id}))
    assert response.status_code == status.HTTP_200_OK, response.data


def test_delete_address(client, fake):
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

    response = client.delete(reverse("address", kwargs={"pk": address.id}))
    assert response.status_code == status.HTTP_200_OK
    assert Address.objects.filter(pk=address.id).exists() is False
