import pytest
from django.contrib.gis.geos import Point
from django.db import DataError, IntegrityError

from backend.models import Address, ContactType, Contact

pytestmark = pytest.mark.usefixtures("db")


@pytest.mark.parametrize("field,length", (
        ("first_name", 25),
        ("last_name", 25),
        ("email", 75),
        ("phone", 25)
))
def test_max_length(field, length, fake):
    state = fake.state_abbr()
    address = Address(
        point=Point(1, 2),
        creator_user_id="hello id",
        last_updated_user_id="hello id",
        neighborhood="some neighborhood",
        street=fake.street_name(),
        city=fake.city(),
        state=state,
        zip=fake.postalcode()
    )
    address.save()
    address.refresh_from_db()

    ct = ContactType(slug="some-slug")
    ct.save()
    ct.refresh_from_db()

    data = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "phone": fake.phone_number()
    }

    val = "".join("x" for _ in range(length + 1))
    data[field] = val

    contact = Contact(**data)
    with pytest.raises(DataError) as exc:
        contact.save()
    assert str(exc.value.args[0]) == f"value too long for type character varying({length})\n"


def test_email_unique(fake):
    state = fake.state_abbr()
    address = Address(
        point=Point(1, 2),
        creator_user_id="hello id",
        last_updated_user_id="hello id",
        neighborhood="some neighborhood",
        street=fake.street_name(),
        city=fake.city(),
        state=state,
        zip=fake.postalcode()
    )
    address.save()
    address.refresh_from_db()

    ct = ContactType(slug="some-slug")
    ct.save()
    ct.refresh_from_db()

    email = fake.email()
    c1 = Contact(
        address=address,
        contact_type=ct,
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=email,
        phone=fake.phone_number()
    )
    c1.save()

    c2 = Contact(
        address=address,
        contact_type=ct,
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=email,
        phone=fake.phone_number()
    )
    with pytest.raises(IntegrityError) as exc:
        c2.save()

    assert "duplicate key value violates unique constraint" in str(exc.value.args[0])
