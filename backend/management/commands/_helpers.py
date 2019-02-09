from django.db import IntegrityError

from backend.models import ContactType


def init_contact_types(cmd):
    """
    Writes valid ContactTypes to db
    :param cmd: Django BaseCommand 'self' reference
    """
    for name, value in ContactType.Types:
        try:
            ct = ContactType(slug=value)
            ct.save()
        except IntegrityError:
            cmd.writer.write(
                cmd.style.ERROR(f"contact_type: '{name}' already exists")
            )
    cmd.writer.write(cmd.style.SUCCESS("types written"))
