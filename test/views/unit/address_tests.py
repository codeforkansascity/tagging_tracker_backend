from django.urls import reverse
from rest_framework import status

from backend.models import Address
from backend.views.address import AddressView, AddressListView, AddressTagsView


def test_address_view_permissions_set():
    scopes = {
        "get": "read:address",
        "delete": "write:address"
    }
    assert AddressView().scopes == scopes, "Invalid permissions"


def test_address_list_view_permissions_set():
    scopes = {
        "get": "read:address",
        "post": "write:address"
    }
    assert AddressListView().scopes == scopes, "Invalid permissions"


def test_address_tags_view_permissions_set():
    scopes = {"get": "read:address"}
    assert AddressTagsView().scopes == scopes, "Invalid permissions"


def test_get_address_found_and_returned(request_builder, mocker):
    pk = 1

    get_or_404 = mocker.patch("backend.views.address.get_object_or_404")
    serializer = mocker.patch("backend.views.address.AddressSerializer")
    expected_data = "hello"
    serializer.return_value.data = expected_data

    request = request_builder("GET", reverse("address", kwargs={"pk": pk}))
    response = AddressView().get(request, pk)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data
    get_or_404.assert_called_once_with(Address, pk=pk)
    serializer.assert_called_once_with(get_or_404.return_value)


def test_get_address_delete_found_and_deleted(request_builder, mocker):
    pk = 1

    get_or_404 = mocker.patch("backend.views.address.get_object_or_404")

    request = request_builder("DELETE", reverse("address", kwargs={"pk": pk}))
    response = AddressView().delete(request, pk)

    assert response.status_code == status.HTTP_200_OK
    get_or_404.assert_called_once_with(Address, pk=pk)
    get_or_404.return_value.delete.assert_called_once()


def test_get_address_list_returns_all(request_builder, mocker):
    address_all = mocker.patch("backend.views.address.Address.objects.all")

    request = request_builder("GET", reverse("address-list"))
    response = AddressListView().get(request)

    assert response.status_code == status.HTTP_200_OK
    address_all.assert_called_once()


def test_post_address_list_invalid_parameters_response_structure(request_builder, mocker):
    is_valid = mocker.patch("backend.views.address.AddressSerializer.is_valid")
    is_valid.return_value = False

    errors = mocker.patch("backend.views.address.AddressSerializer.errors", new_callable=mocker.PropertyMock)
    expected_return = {"parameter": ["error"]}
    errors.return_value = expected_return

    request = request_builder("POST", reverse("address-list"))
    response = AddressListView().post(request)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == expected_return


def test_post_address_list_valid_parameters_valid_response_structure(request_builder, mocker):
    address_serializer = mocker.patch("backend.views.address.AddressSerializer")
    address_serializer.return_value.is_valid.return_value = True

    expected_data = {"key": "value"}
    address_serializer.return_value.data = expected_data

    request = request_builder("POST", reverse("address-list"))
    response = AddressListView().post(request)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == expected_data


def test_get_address_tags_response_structure(request_builder, mocker):
    pk = 1

    mocker.patch("backend.views.address.get_object_or_404")
    mocker.patch("backend.views.address.Tag.objects.filter")
    tag_serializer = mocker.patch("backend.views.address.TagSerializer")

    request = request_builder("GET", reverse("address-tags", kwargs={"pk": pk}))

    response = AddressTagsView().get(request, pk)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == tag_serializer.return_value.data
