import pytest
from django.contrib.gis.geos import Point
from schema import Schema, And, Or, Use

from backend.models import Address
from backend.serializers import AddressSerializer
from test.serializers.schema import is_blank

pytestmark = pytest.mark.usefixtures("db")


ADDRESS_SCHEMA = Schema({
    "id": int,
    "type": str,
    "geometry": And(
        Use(dict),
        {
            "type": str,
            "coordinates": [float, float]
        }
    ),
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
            "owner_name": Or(str, is_blank),
            "owner_contact_number": Or(str, is_blank),
            "owner_email": Or(str, is_blank),
            "tenant_name": Or(str, is_blank),
            "tenant_phone": Or(str, is_blank),
            "tenant_email": Or(str, is_blank),
            "follow_up_owner_needed": bool,
            "land_bank_property": bool,
            "type_of_property": int,
            "date_updated": str
        }
    )
})


def test_schema(fake):
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

    data = AddressSerializer(address).data
    ADDRESS_SCHEMA.validate(dict(data))
