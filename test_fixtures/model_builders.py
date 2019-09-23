import pytest

from django.contrib.gis.geos import Point
from django.utils import timezone

from backend.models import PropertyType, Address, Tag, ContactType, Contact


@pytest.fixture()
def property_type_builder():
    def _builder(slug: str = "some-slug"):
        pt = PropertyType(slug=slug)
        pt.save()
        pt.refresh_from_db()
        return pt

    return _builder


@pytest.fixture()
def address_builder(fake, property_type_builder):
    def _builder(property_type: PropertyType = None, **kwargs):
        if property_type is None:
            property_type = property_type_builder(**kwargs)

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
            property_type=property_type,
        )
        address.save()
        address.refresh_from_db()
        return address

    return _builder


@pytest.fixture()
def tag_builder(fake, address_builder):
    def _builder(address: Address = None, **kwargs):
        if address is None:
            address = address_builder(**kwargs)

        tag = Tag(
            address=address,
            creator_user_id="some id",
            last_updated_user_id="some id",
            date_taken=timezone.now(),
            description=fake.text(),
        )
        tag.save()
        tag.refresh_from_db()
        return tag

    return _builder


@pytest.fixture()
def contact_type_builder():
    def _builder(slug: str = "some-slug"):
        ct = ContactType(slug=slug)
        ct.save()
        ct.refresh_from_db()
        return ct

    return _builder


@pytest.fixture()
def contact_builder(fake, address_builder, contact_type_builder):
    def _builder(address: Address = None, contact_type: ContactType = None, **kwargs):
        if address is None:
            address = address_builder(**kwargs)
        if contact_type is None:
            contact_type = contact_type_builder(**kwargs)

        contact = Contact(
            address=address,
            contact_type=contact_type,
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            phone=fake.phone_number(),
        )
        contact.save()
        contact.refresh_from_db()
        return contact

    return _builder
