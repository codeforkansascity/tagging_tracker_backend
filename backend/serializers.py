from backend.models import Tag, Address, Contact, ContactType
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


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"


class ContactTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactType
        fields = "__all__"
