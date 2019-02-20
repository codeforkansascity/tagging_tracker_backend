import pytest

from backend.models import Contact


@pytest.mark.parametrize("field,max_length", (
        ("first_name", 25),
        ("last_name", 25),
        ("email", 75),
        ("phone", 25),
))
def test_max_lenths(field, max_length):
    assert Contact._meta.get_field(field).max_length == max_length


def test_default_values():
    assert Contact._meta.get_field("follow_up").default is False


def test_unique_fields():
    assert Contact._meta.get_field("email").unique is True
