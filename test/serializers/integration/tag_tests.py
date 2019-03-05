import pytest
from django.contrib.gis.geos import Point
from django.utils import timezone
from schema import Schema, Or

from backend.models import Tag, Address, PropertyType
from backend.serializers import TagSerializer
from test.serializers.schema import is_blank, is_datetime

pytestmark = pytest.mark.usefixtures("db")

TAG_SCHEMA = Schema(
    {
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
        "racially_motivated": bool,
        "square_footage": Or(str, is_blank),
        "surface": Or(str, is_blank),
        "tag_words": Or(str, is_blank),
        "tag_initials": Or(str, is_blank),
    }
)


def test_schema(fake):
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
    address.refresh_from_db()

    tag = Tag(
        address=address,
        creator_user_id="some id",
        last_updated_user_id="some id",
        date_taken=timezone.now(),
        description=fake.text(),
    )
    tag.save()
    tag.refresh_from_db()

    data = TagSerializer(tag).data
    TAG_SCHEMA.validate(dict(data))
