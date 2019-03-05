from django.core.management import BaseCommand
from django.db import IntegrityError

from backend.models import ContactType, PropertyType


def init_contact_types(cmd: BaseCommand):
    """
    Writes valid ContactTypes to db
    :param cmd: Django BaseCommand 'self' reference
    """
    for name, value in ContactType.Types:
        try:
            ct = ContactType(slug=value)
            ct.save()
        except IntegrityError:
            cmd.stdout.write(cmd.style.ERROR(f"contact_type: '{name}' already exists"))
    cmd.stdout.write(cmd.style.SUCCESS("contact types written"))


def init_property_types(cmd: BaseCommand):
    """
    Writes valid PropertyTypes to db
    :param cmd: Django BaseCommand 'self' reference
    """
    for name, value in PropertyType.Types:
        try:
            pt = PropertyType(slug=value)
            pt.save()
        except IntegrityError:
            cmd.stdout.write(cmd.style.ERROR(f"property_type: '{name}' already exists"))
    cmd.stdout.write(cmd.style.SUCCESS("property types written"))
