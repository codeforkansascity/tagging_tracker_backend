from django.contrib.gis.geos import Point
from django.core.management import BaseCommand
from django.utils import timezone
from faker import Faker

from backend.management.commands._helpers import init_contact_types, init_property_types
from backend.models import Address, Tag, Contact, ContactType, PropertyType


class Command(BaseCommand):
    help = "Seed database with fake data"

    def handle(self, *args, **options):
        init_contact_types(self)
        init_property_types(self)

        fake = Faker()

        address = Address(
            point=Point(1, 2),
            creator_user_id="some id",
            last_updated_user_id="some other id",
            neighborhood="some neighborhood",
            street=fake.street_address(),
            city="Kansas City",
            state="MO",
            zip="64030",
            land_bank_property=False,
            property_type=PropertyType.objects.get(
                slug=PropertyType.Types.COMMERCIAL.value
            ),
        )
        address.save()
        address.refresh_from_db()

        contact = Contact(
            address=address,
            contact_type=ContactType.objects.get(slug=ContactType.Types.OWNER.value),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            phone=fake.phone_number(),
        )
        contact.save()

        tag = Tag(
            address=address,
            creator_user_id="some id",
            last_updated_user_id="some id",
            date_taken=timezone.now(),
            description=fake.text(),
            img="some resource url",
            square_footage="23",
            surface="concrete",
            tag_words="some words",
            tag_initials="some initials",
        )
        tag.save()

        self.stdout.write(self.style.SUCCESS("Successfully created data"))
