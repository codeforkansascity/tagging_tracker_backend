from django.db import IntegrityError

from backend.models import ContactType


def init_contact_types(writer, style):
    for name, value in ContactType.Types:
        try:
            ct = ContactType(slug=value)
            ct.save()
        except IntegrityError:
            writer.write(
                style.ERROR(f"contact_type: '{name}' already exists")
            )
    writer.write(style.SUCCESS("types written"))
