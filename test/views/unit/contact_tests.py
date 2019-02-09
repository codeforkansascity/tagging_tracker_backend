from rest_framework import status
from rest_framework.parsers import JSONParser

from backend.views.contacts import ContactListView, ContactView


def test_contact_list_parser_class_set():
    assert ContactListView().parser_classes == (JSONParser,)


def test_contact_view_parser_class_set():
    assert ContactView().parser_classes == (JSONParser,)


def test_contact_list_post_invalid_response_structure(mocker, request_builder):
    pk = 1
    get_obj_mock = mocker.patch("backend.views.contacts.get_object_or_404")
    serializer_mock = mocker.patch("backend.views.contacts.ContactSerializer")

    serializer_mock.return_value.is_valid.return_value = False

    request = request_builder("post", "/endpoint", {"some": "data"})

    response = ContactListView().post(request, pk)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == serializer_mock.return_value.errors


def test_contact_view_put_invalid_response_structure(mocker, request_builder):
    pk = 1
    address_pk = 1
    get_obj_mock = mocker.patch("backend.views.contacts.get_object_or_404")
    serializer_mock = mocker.patch("backend.views.contacts.ContactSerializer")

    serializer_mock.return_value.is_valid.return_value = False

    request = request_builder("put", "/endpoint", {"id": pk})

    response = ContactView().put(request, address_pk, pk)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == serializer_mock.return_value.errors
