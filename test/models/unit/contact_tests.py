import pytest
from django.db.models import CASCADE

from backend.models import Contact, Address, ContactType


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


@pytest.mark.parametrize("field,model,on_delete", (
        ("address", Address, CASCADE),
        ("contact_type", ContactType, CASCADE)
))
def test_foreign_keys(field, model, on_delete):
    field_obj = Contact._meta.get_field(field)
    assert field_obj.remote_field.on_delete == on_delete
    assert field_obj.remote_field.model == model
