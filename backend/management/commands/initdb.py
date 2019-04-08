from django.core.management import BaseCommand

from backend.management.commands._helpers import init_contact_types, init_property_types


class Command(BaseCommand):
    help = "Initializes database with proper values"

    def handle(self, *args, **options):
        init_contact_types(self)
        init_property_types(self)
