from django.core.management import BaseCommand
from django.db import IntegrityError

from backend.models import ContactType


class Command(BaseCommand):
    help = "Initializes database with proper values"

    def handle(self, *args, **options):

        for name, value in ContactType.Types:
            try:
                ct = ContactType(slug=value)
                ct.save()
            except IntegrityError:
                self.stdout.write(
                    self.style.ERROR(f"contact_type: '{name}' already exists")
                )
        self.stdout.write(self.style.SUCCESS("types written"))
