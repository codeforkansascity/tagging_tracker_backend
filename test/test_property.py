from django.http import JsonResponse, HttpRequest
from django.test import TestCase

from backend.controllers import property
from backend.controllers.controller_utils import HTTP_STATUS_METHOD_NOT_ALLOWED
from backend.models import PropertyType
from backend.serializers import PropertyTypeSerializer


class TestPropertyType(TestCase):
    request = HttpRequest()
    property_types = []

    def setUp(self):
        for i in range(5):
            self.property_types.append(PropertyType.objects.create(type_name="house"))

    def tearDown(self):
        PropertyType.objects.all().delete()
        self.property_types.clear()

    def test_property_type_list__get(self):
        self.request.method = 'GET'
        response = property.property_type_list(self.request)
        actual = response.getvalue().decode("utf-8")

        serializer = PropertyTypeSerializer(self.property_types, many=True)
        expected = JsonResponse(serializer.data, safe=False).getvalue().decode("utf-8")

        self.assertEqual(actual, expected)

    def test_property_type_list__invalid_method(self):
        self.request.method = 'PUT'
        response = property.property_type_list(self.request)
        self.assert_(response.status_code == HTTP_STATUS_METHOD_NOT_ALLOWED)
