from django.core.management import BaseCommand
from django.db import IntegrityError

from backend.models import ContactType
from backend.enums import ContactTypes


class Command(BaseCommand):
    help = "Initializes database with proper values"

    def handle(self, *args, **options):

        for name, value in ContactTypes:
            try:
                ct = ContactType(slug=value)
                ct.save()
            except IntegrityError:
                self.stdout.write(
                    self.style.ERROR(f"contact_type: '{name}' already exists")
                )
        self.stdout.write(self.style.SUCCESS("types written"))
