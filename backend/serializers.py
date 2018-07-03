from backend.models import Tag, Address
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

class AddressSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Address
        geo_field = "point"
        fields = (
          'id',
          'neighborhood',
          'street',
          'city',
          'state',
          'zip',
          'creator_user_id',
          'last_updated_user_id',
          'owner_name',
          'owner_contact_number',
          'owner_email',
          'tenant_name',
          'tenant_phone',
          'tenant_email',
          'follow_up_owner_needed',
          'land_bank_property',
          'type_of_property',
          'date_updated'
        )

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
          'id',
          'address',
          'creator_user_id',
          'crossed_out',
          'date_taken',
          'date_updated',
          'description',
          'gang_related',
          'img',
          'last_updated_user_id',
          'racially_motivated',
          'square_footage',
          'surface',
          'tag_words',
          'tag_initials'
        )
