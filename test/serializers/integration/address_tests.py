import pytest
from schema import Schema, And, Use

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


def test_address_schema(address_builder):
    address = address_builder()

    data = AddressSerializer(address).data
    ADDRESS_SCHEMA.validate(dict(data))


def test_property_type_schema(property_type_builder):
    pt = property_type_builder()

    data = PropertyTypeSerializer(pt).data
    PROPERTY_TYPE_SCHEMA.validate(dict(data))
