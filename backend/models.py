import logging
import os

from django.conf import settings
from django.db import models
from django.contrib.gis.db.models import PointField, GeoManager
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from azure.storage.blob import BlockBlobService

logger = logging.getLogger(__name__)


class Address(models.Model):
    objects = GeoManager()
    point = PointField(srid=4326)
    creator_user_id = models.CharField(max_length=255)
    last_updated_user_id = models.CharField(max_length=255)
    neighborhood = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=12)
    owner_name = models.CharField(max_length=100, blank=True)
    owner_contact_number = models.CharField(max_length=20, blank=True)
    owner_email = models.CharField(max_length=100, blank=True)
    tenant_name = models.CharField(max_length=100, blank=True)
    tenant_phone = models.CharField(max_length=100, blank=True)
    tenant_email = models.CharField(max_length=100, blank=True)
    follow_up_owner_needed = models.BooleanField(default=False)
    land_bank_property = models.BooleanField(default=False)
    type_of_property = models.IntegerField(default=False, blank=False)
    date_updated = models.DateTimeField(auto_now=True)

    @property
    def latitude(self):
        return self.point.y

    @property
    def longitude(self):
        return self.point.x

    def __str__(self):
        return self.street


class Tag(models.Model):
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    creator_user_id = models.CharField(max_length=255)
    last_updated_user_id = models.CharField(max_length=255)
    crossed_out = models.BooleanField(default=False)
    date_updated = models.DateTimeField(auto_now=True)
    date_taken = models.DateTimeField()
    description = models.CharField(max_length=255)
    gang_related = models.BooleanField(default=False)
    img = models.CharField(max_length=1000, blank=True)
    neighborhood = models.CharField(max_length=255, blank=True)
    racially_motivated = models.BooleanField(default=False)
    square_footage = models.CharField(max_length=50, blank=True)
    surface = models.CharField(max_length=100, blank=True)
    tag_words = models.CharField(max_length=255, blank=True)
    tag_initials = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.address} {self.id}"


@receiver(pre_delete, sender=Tag)
def delete_image(sender, instance, **kwargs):
    image_name = instance.img.split("/")[-1]
    if not settings.DEBUG:
        block_blob_service = BlockBlobService(account_name=os.environ['AZURE_IMAGE_CONTAINER_NAME'], account_key=os.environ['AZURE_IMAGE_CONTAINER_KEY'])
        block_blob_service.delete_blob('images', image_name)
        logger.debug(f"Image: {image_name} deleted from Azure")
    else:
        logger.debug(f"Image: {image_name} would of been deleted if not in DEBUG mode")
