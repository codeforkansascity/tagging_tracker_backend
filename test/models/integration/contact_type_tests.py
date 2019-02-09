import pytest
from django.db import DataError, IntegrityError

from backend.models import ContactType

pytestmark = pytest.mark.usefixtures("db")


def test_slug_max_length():
    value = "".join("x" for _ in range(16))

    ct = ContactType(slug=value)

    with pytest.raises(DataError) as exc:
        ct.save()
    assert str(exc.value.args[0]) == "value too long for type character varying(15)\n"


def test_slug_unique():
    ct1 = ContactType(slug="slug")
    ct1.save()

    ct2 = ContactType(slug="slug")

    with pytest.raises(IntegrityError) as exc:
        ct2.save()
    assert "duplicate key value violates unique constraint" in str(exc.value.args[0])
