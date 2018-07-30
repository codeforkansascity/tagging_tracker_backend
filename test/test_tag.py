from datetime import date
from django.contrib.gis.geos import Point
from django.db.models import signals
from django.http import HttpRequest, JsonResponse
from django.test import TestCase

from backend.controllers.tag import TagResource
from backend.controllers.controller_utils import HTTP_STATUS_NOT_FOUND, HTTP_STATUS_METHOD_NOT_ALLOWED
from backend.models import Tag, Address, delete_image
from backend.serializers import TagSerializer


class TestTag(TestCase):
    tag_resource = TagResource()
    request = HttpRequest()
    tags = []

    def setUp(self):
        address = Address.objects.create(point=Point(50, 50), street="1234 Main St", state="MO", zip="12345",
                                         type_of_property=0)
        for i in range(5):
            self.tags.append(Tag.objects.create(address=address, creator_user_id=i, last_updated_user_id=i+1,
                                                date_taken=("%sT00:00:00Z" % date.today()), description=("tag%d" % i)))

    def tearDown(self):
        signals.pre_delete.disconnect(receiver=delete_image, sender=Tag)
        Tag.objects.all().delete()
        signals.pre_delete.connect(receiver=delete_image, sender=Tag)

        self.tags.clear()

    def test_tag_list__get(self):
        self.request.method = 'GET'
        response = self.tag_resource.tag_list(self.request)
        actual = response.getvalue().decode("utf-8")

        serializer = TagSerializer(self.tags, many=True)
        expected = JsonResponse(serializer.data, safe=False).getvalue().decode("utf-8")

        self.assertEqual(actual, expected)

    def test_tag_list__invalid_method(self):
        self.request.method = 'PUT'
        response = self.tag_resource.tag_list(self.request)
        self.assert_(response.status_code == HTTP_STATUS_METHOD_NOT_ALLOWED)

    def test_tag_detail__get(self):
        self.request.method = 'GET'
        pk = self.tags[0].id
        response = self.tag_resource.tag_detail(self.request, pk)
        actual = response.getvalue().decode("utf-8")

        serializer = TagSerializer(self.tags[0])
        expected = JsonResponse(serializer.data, safe=False).getvalue().decode("utf-8")

        self.assertEqual(actual, expected)

    def test_tag_detail__invalid_method(self):
        self.request.method = 'POST'
        pk = self.tags[0].id
        response = self.tag_resource.tag_detail(self.request, pk)
        self.assert_(response.status_code == HTTP_STATUS_METHOD_NOT_ALLOWED)

    def test_tag_detail__invalid_tag(self):
        self.request.method = 'GET'
        pk = None
        response = self.tag_resource.tag_detail(self.request, pk)
        self.assert_(response.status_code == HTTP_STATUS_NOT_FOUND)
