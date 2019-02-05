from django.contrib.gis.geos import Point
from django.core.management import BaseCommand
from django.utils import timezone
from faker import Faker

from backend.models import Address, Tag


class Command(BaseCommand):
    help = "Seed database with fake data"


    def handle(self, *args, **options):
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
            owner_name=fake.name(),
            owner_email=fake.safe_email(),
            tenant_name=fake.name(),
            tenant_email=fake.safe_email(),
            follow_up_owner_needed=True,
            land_bank_property=False,
            type_of_property=1,
        )
        address.save()
        address.refresh_from_db()

        tag = Tag(
            address=address,
            creator_user_id="some id",
            last_updated_user_id="some id",
            date_taken=timezone.now(),
            description=fake.text(),
            img="some resource url",
            neighborhood="the neighborhood",
            square_footage="23",
            surface="concrete",
            tag_words="some words",
            tag_initials="some initials"
        )
        tag.save()

        self.stdout.write(self.style.SUCCESS("Successfully created data"))
