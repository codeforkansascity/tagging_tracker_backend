import pytest
from django.contrib.gis.geos import Point
from django.db.models import Field

from backend.models import Address, PropertyType


def test_longitude_returns_x(fake):
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
    )

    assert address.longitude == 1


def test_latitude_returns_y(fake):
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
    )

    assert address.latitude == 2


@pytest.mark.parametrize("field,max_length", (
        ("creator_user_id", 255),
        ("last_updated_user_id", 255),
        ("neighborhood", 255),
        ("street", 255),
        ("city", 255),
        ("state", 100),
        ("zip", 12),
))
def test_max_lengths(field, max_length):
    assert Address._meta.get_field(field).max_length == max_length


@pytest.mark.parametrize("field,default", (
        ("land_bank_property", False),
        ("type_of_property", False),
))
def test_defaults(field, default):
    assert Address._meta.get_field(field).default == default


def test_date_updated_auto_now_is_true():
    assert Address._meta.get_field("date_updated").auto_now is True
