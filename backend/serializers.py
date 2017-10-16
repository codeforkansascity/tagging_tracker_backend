from rest_framework import serializers
from backend.models import TaggingPoint
from rest_framework_gis.serializers import GeoFeatureModelSerializer



class TaggingPointSerializer(GeoFeatureModelSerializer):
    model = TaggingPoint
    geo_field = "point"

    fields = ('id', 'address', 'city', 'state')