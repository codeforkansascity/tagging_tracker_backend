import pytest
from schema import Schema, Or

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


def test_schema(tag_builder):
    tag = tag_builder()

    data = TagSerializer(tag).data
    TAG_SCHEMA.validate(dict(data))
