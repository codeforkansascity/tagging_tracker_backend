from django.core.management import BaseCommand
from django.db import IntegrityError

from backend.models import ContactType, ContactTypes


class Command(BaseCommand):
    help = "Initializes database with proper values"

    def handle(self, *args, **options):

        for type in ContactTypes:
            try:
                ct = ContactType(slug=type.value)
                ct.save()
            except IntegrityError:
                self.stdout.write(
                    self.style.ERROR(f"contact_type: '{type}' already exists")
                )
        self.stdout.write(self.style.SUCCESS("types written"))
