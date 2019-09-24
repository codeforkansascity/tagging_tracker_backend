import pytest
from schema import Schema

from backend.serializers import ContactSerializer, ContactTypeSerializer

pytestmark = pytest.mark.usefixtures("db")

CONTACT_SCHEMA = Schema(
    {
        "id": int,
        "address": int,
        "contact_type": int,
        "first_name": str,
        "last_name": str,
        "email": str,
        "phone": str,
        "follow_up": bool,
    }
)

CONTACT_TYPE_SCHEMA = Schema({"id": int, "slug": str})


def test_contact_schema(contact_builder):
    contact = contact_builder()

    data = dict(ContactSerializer(contact).data)

    CONTACT_SCHEMA.validate(data)


def test_contact_type_schema(contact_type_builder):
    ct = contact_type_builder()

    data = dict(ContactTypeSerializer(ct).data)

    CONTACT_TYPE_SCHEMA.validate(data)
