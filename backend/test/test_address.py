from django.contrib.gis.geos import Point
from django.db.models import signals
from django.http import HttpRequest, JsonResponse
from django.test import TestCase
from random import randint

from backend.controllers import address
from backend.models import Address, delete_image
from backend.serializers import AddressSerializer


STATUS_CODES = {"No Content": 204, "Unauthorized": 401, "Not Found": 404, "Method Not Allowed": 405}


class TestAddress(TestCase):
    request = HttpRequest()
    addresses = []

    def setUp(self):
        for i in range(5):
            self.addresses.append(Address.objects.create(point=Point(randint(0, 89), randint(0, 179)),
                                                         street=f"{randint(1000, 9999)} Main St",
                                                         state="MO", zip=randint(10000, 99999),
                                                         type_of_property=0))

    def tearDown(self):
        signals.pre_delete.disconnect(receiver=delete_image, sender=Address)
        Address.objects.all().delete()
        signals.pre_delete.connect(receiver=delete_image, sender=Address)

        self.addresses.clear()

    def test_address_list__get(self):
        self.request.method = 'GET'
        response = address.address_list(self.request)
        actual = response.getvalue().decode("utf-8")

        serializer = AddressSerializer(self.addresses, many=True)
        expected = JsonResponse(serializer.data, safe=False).getvalue().decode("utf-8")

        self.assertEqual(actual, expected)


    # TODO add valid token to this test's authorization request
    '''
    def test_address_list__post__auth(self):
        self.request.method = 'POST'
        self.request.META['HTTP_AUTHORIZATION'] = "BEARER "
        self.request._body = AddressSerializer(self.addresses[0])

        response = address.address_list(self.request)
        self.assert_(response.status_code == STATUS_CODES['No Content'])
    '''

    def test_address_list__post__unauth(self):
        self.request.method = 'POST'
        self.request.META['HTTP_AUTHORIZATION'] = "BEARER fake_token"
        self.request._body = AddressSerializer(self.addresses[0])

        response = address.address_list(self.request)
        self.assert_(response.status_code == STATUS_CODES['Unauthorized'])

    def test_address_list__invalid_method(self):
        self.request.method = 'PUT'
        response = address.address_list(self.request)
        self.assert_(response.status_code == STATUS_CODES['Method Not Allowed'])

    def test_address_detail__get(self):
        self.request.method = 'GET'
        pk = self.addresses[0].id
        response = address.address_detail(self.request, pk)
        actual = response.getvalue().decode("utf-8")

        serializer = AddressSerializer(self.addresses[0])
        expected = JsonResponse(serializer.data, safe=False).getvalue().decode("utf-8")

        self.assertEqual(actual, expected)

    # TODO add valid token to this test's authorization request
    '''
    def test_address_detail__delete__auth(self):
        self.request.method = 'DELETE'
        self.request.META['HTTP_AUTHORIZATION'] = "BEARER "
        pk = self.addresses[0].id

        response = address.address_detail(self.request, pk)
        self.assert_(response.status_code == STATUS_CODES['No Content'])
    '''
    
    def test_address_detail__delete__unauth(self):
        self.request.method = 'DELETE'
        self.request.META['HTTP_AUTHORIZATION'] = "BEARER fake_token"
        pk = self.addresses[0].id

        response = address.address_detail(self.request, pk)
        self.assert_(response.status_code == STATUS_CODES['Unauthorized'])

    def test_address_detail__invalid_method(self):
        self.request.method = 'POST'
        pk = self.addresses[0].id
        response = address.address_detail(self.request, pk)
        self.assert_(response.status_code == STATUS_CODES['Method Not Allowed'])

    def test_address_detail__invalid_address(self):
        self.request.method = 'GET'
        pk = None
        response = address.address_detail(self.request, pk)
        self.assert_(response.status_code == STATUS_CODES['Not Found'])

    # TODO add tests for address_tags() once it works as intended
