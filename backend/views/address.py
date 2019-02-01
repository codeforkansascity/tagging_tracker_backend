import logging
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.models import Address, Tag
from backend.serializers import AddressSerializer, TagSerializer

logger = logging.getLogger(__name__)


class AddressView(APIView):

    def get(self, request, pk):
        address = get_object_or_404(Address, pk=pk)
        return Response(AddressSerializer(address).data)

    def delete(self, request, pk):
        address = get_object_or_404(Address, pk=pk)
        data = {
            "street": address.street,
            "city": address.city,
            "zip": address.zip
        }
        address.delete()
        logger.debug(f"{data['street']} {data['city']}, {data['zip']} deleted")
        return Response()


class AddressListView(APIView):

    parser_classes = (JSONParser,)

    def get(self, request):
        addresses = Address.objects.all()
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            logger.debug(f"id: {obj.id} created by {obj.creator_user_id}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressTagsView(APIView):

    def get(self, request, pk):
        address = get_object_or_404(Address, pk=pk)
        tags = Tag.objects.filter(address=address)
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)
