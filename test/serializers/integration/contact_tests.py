import pytest
from django.contrib.gis.geos import Point
from schema import Schema

from backend.models import Address, ContactType, Contact, PropertyType
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


def test_contact_schema(fake):
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

    ct = ContactType(slug="some-slug")
    ct.save()
    ct.refresh_from_db()

    contact = Contact(
        address=address,
        contact_type=ct,
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email(),
        phone=fake.phone_number(),
    )
    contact.save()
    contact.refresh_from_db()

    data = dict(ContactSerializer(contact).data)

    CONTACT_SCHEMA.validate(data)


def test_contact_type_schema():
    ct = ContactType(slug="some-slug")
    ct.save()
    ct.refresh_from_db()

    data = dict(ContactTypeSerializer(ct).data)

    CONTACT_TYPE_SCHEMA.validate(data)
