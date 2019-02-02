from backend.models import Tag, Address
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class AddressSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Address
        geo_field = "point"
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
