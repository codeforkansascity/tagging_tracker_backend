from django.contrib.gis.db import models

class Address(models.Model):
    objects = models.GeoManager()
    point = models.PointField(srid=4326)
    creator_user_id = models.CharField(max_length=255)
    last_updated_user_id = models.CharField(max_length=255)
    neighborhood = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=12)
    owner_name = models.CharField(max_length=12, blank=True)
    owner_contact_number = models.CharField(max_length=12, blank=True)
    owner_email = models.CharField(max_length=12, blank=True)
    tenant_name = models.CharField(max_length=12, blank=True)
    tenant_phone = models.CharField(max_length=12, blank=True)
    tenant_email = models.CharField(max_length=12, blank=True)
    owner_email = models.CharField(max_length=12, blank=True)
    follow_up_owner_needed = models.BooleanField(default=False)
    land_bank_property = models.BooleanField(default=False)
    date_updated = models.DateField(auto_now=True)

    def latitude(self):
        return self.point.y

    def longitude(self):
        return self.point.x

class Tag(models.Model):
  address = models.ForeignKey('Address')
  creator_user_id = models.CharField(max_length=255)
  last_updated_user_id = models.CharField(max_length=255)
  crossed_out = models.BooleanField(default=False)
  date_updated = models.DateField(auto_now=True)
  description = models.CharField(max_length=255)
  gang_related = models.BooleanField(default=False)
  img = models.CharField(max_length=1000, blank=True)
  neighborhood = models.CharField(max_length=255, blank=True)
  racially_motivated = models.BooleanField(default=False)
  square_footage = models.CharField(max_length=50, blank=True)
  surface = models.CharField(max_length=100, blank=True)
  tag_words = models.CharField(max_length=255, blank=True)
  tag_initials = models.CharField(max_length=20, blank=True)
