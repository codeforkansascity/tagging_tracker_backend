import pytest
from django.contrib.gis.geos import Point
from schema import Schema, And, Use

from backend.models import Address, PropertyType
from backend.serializers import AddressSerializer, PropertyTypeSerializer

pytestmark = pytest.mark.usefixtures("db")


ADDRESS_SCHEMA = Schema(
    {
        "id": int,
        "type": str,
        "geometry": And(Use(dict), {"type": str, "coordinates": [float, float]}),
        "properties": And(
            Use(dict),
            {
                "neighborhood": str,
                "street": str,
                "city": str,
                "state": str,
                "zip": str,
                "creator_user_id": str,
                "last_updated_user_id": str,
                "land_bank_property": bool,
                "property_type": int,
                "date_updated": str,
            },
        ),
    }
)

PROPERTY_TYPE_SCHEMA = Schema({"id": int, "slug": str})


def test_address_schema(fake):
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

    data = AddressSerializer(address).data
    ADDRESS_SCHEMA.validate(dict(data))


def test_property_type_schema():
    pt = PropertyType(slug="some_slug")
    pt.save()

    data = PropertyTypeSerializer(pt).data
    PROPERTY_TYPE_SCHEMA.validate(dict(data))
