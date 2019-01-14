import os

from django.db import models as base_models
from django.contrib.gis.db import models as gis_models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from azure.storage.blob import BlockBlobService


class Address(gis_models.Model):
    objects = gis_models.GeoManager()
    point = gis_models.PointField(srid=4326)
    creator_user_id = gis_models.CharField(max_length=255)
    last_updated_user_id = gis_models.CharField(max_length=255)
    neighborhood = gis_models.CharField(max_length=255)
    street = gis_models.CharField(max_length=255)
    city = gis_models.CharField(max_length=255)
    state = gis_models.CharField(max_length=100)
    zip = gis_models.CharField(max_length=12)
    owner_name = gis_models.CharField(max_length=100, blank=True)
    owner_contact_number = gis_models.CharField(max_length=20, blank=True)
    owner_email = gis_models.CharField(max_length=100, blank=True)
    tenant_name = gis_models.CharField(max_length=100, blank=True)
    tenant_phone = gis_models.CharField(max_length=100, blank=True)
    tenant_email = gis_models.CharField(max_length=100, blank=True)
    follow_up_owner_needed = gis_models.BooleanField(default=False)
    land_bank_property = gis_models.BooleanField(default=False)
    type_of_property = gis_models.IntegerField(default=False, blank=False)
    date_updated = gis_models.DateTimeField(auto_now=True)

    def latitude(self):
        return self.point.y

    def longitude(self):
        return self.point.x

    def __str__(self):
        return self.street


class Tag(base_models.Model):
    address = base_models.ForeignKey(Address, on_delete=base_models.CASCADE)
    creator_user_id = base_models.CharField(max_length=255)
    last_updated_user_id = base_models.CharField(max_length=255)
    crossed_out = base_models.BooleanField(default=False)
    date_updated = base_models.DateTimeField(auto_now=True)
    date_taken = base_models.DateTimeField(auto_now=False)
    description = base_models.CharField(max_length=255)
    gang_related = base_models.BooleanField(default=False)
    img = base_models.CharField(max_length=1000, blank=True)
    neighborhood = base_models.CharField(max_length=255, blank=True)
    racially_motivated = base_models.BooleanField(default=False)
    square_footage = base_models.CharField(max_length=50, blank=True)
    surface = base_models.CharField(max_length=100, blank=True)
    tag_words = base_models.CharField(max_length=255, blank=True)
    tag_initials = base_models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.address} {self.id}"


@receiver(pre_delete, sender=Tag)
def delete_image(sender, instance, **kwargs):
    # TODO: figure out why `settings.DEBUG` appears false despite this logic returning `True`
    debug = True if os.environ.get("DEBUG") else False
    if not debug:
        image_name = instance.img.split("/")[-1]
        block_blob_service = BlockBlobService(account_name=os.environ['AZURE_IMAGE_CONTAINER_NAME'], account_key=os.environ['AZURE_IMAGE_CONTAINER_KEY'])
        block_blob_service.delete_blob('images', image_name)
