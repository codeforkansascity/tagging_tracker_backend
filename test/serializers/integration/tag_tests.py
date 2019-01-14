from datetime import datetime

import pytest
from django.contrib.gis.geos import Point
from schema import Schema, Or

from backend.models import Tag, Address
from backend.serializers import TagSerializer
from test.serializers.schema import is_blank, is_datetime

pytestmark = pytest.mark.usefixtures("db")

TAG_SCHEMA = Schema({
    "id": int,
    "address": int,
    "creator_user_id": str,
    "crossed_out": bool,
    "date_taken": is_datetime,
    "date_updated": is_datetime,
    "description": str,
    "gang_related": bool,
    "img": Or(str, is_blank),
    "last_updated_user_id": str,
    "neighborhood": Or(str, is_blank),
    "racially_motivated": bool,
    "square_footage": Or(str, is_blank),
    "surface": Or(str, is_blank),
    "tag_words": Or(str, is_blank),
    "tag_initials": Or(str, is_blank)
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
    address.refresh_from_db()

    tag = Tag(
        address=address,
        creator_user_id="some id",
        last_updated_user_id="some id",
        date_taken=datetime.utcnow(),
        description=fake.text(),
    )
    tag.save()
    tag.refresh_from_db()

    data = TagSerializer(tag).data
    TAG_SCHEMA.validate(dict(data))
