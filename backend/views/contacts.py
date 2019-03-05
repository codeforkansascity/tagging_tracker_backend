import logging

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.models import Address, Contact, ContactType
from backend.serializers import ContactSerializer, ContactTypeSerializer

logger = logging.getLogger(__name__)


class ContactTypesView(APIView):
    def get(self, request):
        cts = ContactType.objects.all()
        return Response(ContactTypeSerializer(cts, many=True).data)


class ContactView(APIView):

    parser_classes = (JSONParser,)

    def get(self, request, address_pk, pk):
        address = get_object_or_404(Address, pk=address_pk)
        contact = get_object_or_404(Contact, pk=pk, address=address)
        return Response(ContactSerializer(contact).data)

    def put(self, request, address_pk, pk):
        address = get_object_or_404(Address, pk=address_pk)
        contact = get_object_or_404(Contact, pk=pk, address=address)
        data = {**request.data, "address": address.id}
        serializer = ContactSerializer(contact, data=data)
        if serializer.is_valid():
            contact = serializer.save()
            logger.debug(f"contact {contact.id} updated")
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, address_pk, pk):
        address = get_object_or_404(Address, pk=address_pk)
        contact = get_object_or_404(Contact, pk=pk, address=address)
        data = {"id": contact.id, "address": address.id}
        contact.delete()
        logger.debug(f"contact {data['id']} for address {data['address']} deleted")
        return Response()


class ContactListView(APIView):

    parser_classes = (JSONParser,)

    def get(self, request, pk):
        address = get_object_or_404(Address, pk=pk)
        contacts = Contact.objects.filter(address=address)
        return Response(ContactSerializer(contacts, many=True).data)

    def post(self, request, pk):
        address = get_object_or_404(Address, pk=pk)
        data = {**request.data, "address": address.id}
        serializer = ContactSerializer(data=data)
        if serializer.is_valid():
            contact = serializer.save()
            logger.debug(f"contact {contact.id} created")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
