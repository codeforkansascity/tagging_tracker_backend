from backend.models import ContactType


def test_slug_field():
    field = ContactType._meta.get_field("slug")
    assert field.unique is True
    assert field.max_length == 15
