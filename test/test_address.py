from datetime import date
from django.contrib.gis.geos import Point
from django.db.models import signals
from django.http import HttpRequest, JsonResponse
from django.test import TestCase

from backend.controllers import address
from backend.controllers.controller_utils import HTTP_STATUS_NOT_FOUND, HTTP_STATUS_METHOD_NOT_ALLOWED
from backend.models import Address, delete_image, Tag
from backend.serializers import AddressSerializer, TagSerializer


class TestAddress(TestCase):
    request = HttpRequest()
    addresses = []
    tags = []

    def setUp(self):
        for i in range(5):
            self.addresses.append(Address.objects.create(point=Point(50, 50),
                                                         street="1234 Main St",
                                                         state="MO", zip=12345,
                                                         type_of_property=0))

        # create two tags belonging to one address and a third tag belonging to another address
        self.tags.append(Tag.objects.create(address=self.addresses[0], creator_user_id=0, last_updated_user_id=1,
                                            date_taken=f"{date.today()}T00:00:00Z", description="tag0"))
        self.tags.append(Tag.objects.create(address=self.addresses[0], creator_user_id=0, last_updated_user_id=1,
                                            date_taken=f"{date.today()}T00:00:00Z", description="tag1"))
        self.tags.append(Tag.objects.create(address=self.addresses[1], creator_user_id=0, last_updated_user_id=1,
                                            date_taken=f"{date.today()}T00:00:00Z", description="tag2"))

    def tearDown(self):
        signals.pre_delete.disconnect(receiver=delete_image, sender=Tag)
        Tag.objects.all().delete()
        signals.pre_delete.connect(receiver=delete_image, sender=Tag)

        signals.pre_delete.disconnect(receiver=delete_image, sender=Address)
        Address.objects.all().delete()
        signals.pre_delete.connect(receiver=delete_image, sender=Address)

        self.tags.clear()
        self.addresses.clear()

    def test_address_list__get(self):
        self.request.method = 'GET'
        response = address.address_list(self.request)
        actual = response.getvalue().decode("utf-8")

        serializer = AddressSerializer(self.addresses, many=True)
        expected = JsonResponse(serializer.data, safe=False).getvalue().decode("utf-8")

        self.assertEqual(actual, expected)

    def test_address_list__invalid_method(self):
        self.request.method = 'PUT'
        response = address.address_list(self.request)
        self.assert_(response.status_code == HTTP_STATUS_METHOD_NOT_ALLOWED)

    def test_address_detail__get(self):
        self.request.method = 'GET'
        pk = self.addresses[0].id
        response = address.address_detail(self.request, pk)
        actual = response.getvalue().decode("utf-8")

        serializer = AddressSerializer(self.addresses[0])
        expected = JsonResponse(serializer.data, safe=False).getvalue().decode("utf-8")

        self.assertEqual(actual, expected)

    def test_address_detail__invalid_method(self):
        self.request.method = 'POST'
        pk = self.addresses[0].id
        response = address.address_detail(self.request, pk)
        self.assert_(response.status_code == HTTP_STATUS_METHOD_NOT_ALLOWED)

    def test_address_detail__invalid_address(self):
        self.request.method = 'GET'
        pk = None
        response = address.address_detail(self.request, pk)
        self.assert_(response.status_code == HTTP_STATUS_NOT_FOUND)

    def test_retrieve_tags_by_address__get(self):
        self.request.method = 'GET'
        pk = self.addresses[0].id
        response = address.address_tags(self.request, pk)
        actual = response.getvalue().decode("utf=8")

        # filter() used by address_tags() returns list in reverse traversal order
        serializer = TagSerializer(self.tags[-2::-1], many=True)
        expected = JsonResponse(serializer.data, safe=False).getvalue().decode("utf-8")

        self.assertEqual(actual, expected)

    def test_retrieve_tags_by_address__invalid_method(self):
        self.request.method = 'POST'
        pk = self.addresses[0].id
        response = address.address_tags(self.request, pk)
        self.assert_(response.status_code == HTTP_STATUS_METHOD_NOT_ALLOWED)

    def test_retrieve_tags_by_address__invalid_tag(self):
        self.request.method = 'GET'
        pk = None
        response = address.address_tags(self.request, pk)
        self.assert_(response.status_code == HTTP_STATUS_NOT_FOUND)
