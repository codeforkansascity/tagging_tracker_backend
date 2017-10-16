from django.contrib.gis.db import models


# https://gis.stackexchange.com/questions/73322/geodjango-using-lat-lon-to-buffer-from-point
class TaggingPoint(models.Model):
    objects = models.GeoManager()
    point = models.PointField(srid=4326)

    def latitude(self):
        return self.point.y

    def longitude(self):
        return self.point.x
