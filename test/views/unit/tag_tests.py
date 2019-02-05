from django.urls import reverse
from rest_framework import status

from backend.views.tag import TagView, TagListView


def test_tag_view_put_invalid_response_structure(mocker, request_builder):

    get_object = mocker.patch("backend.views.tag.get_object_or_404")
    is_valid = mocker.patch("backend.views.tag.TagSerializer.is_valid")
    is_valid.return_value = False

    errors = mocker.patch("backend.views.tag.TagSerializer.errors", new_callable=mocker.PropertyMock)
    expected_errors = "some error"
    errors.return_value = expected_errors

    pk = 1
    request = request_builder("PUT", reverse("tag", kwargs={"pk": pk}))

    response = TagView().put(request, pk)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == expected_errors


def test_tag_list_post_invalid_response_structure(mocker, request_builder):
    is_valid = mocker.patch("backend.views.tag.TagSerializer.is_valid")
    is_valid.return_value = False

    errors = mocker.patch("backend.views.tag.TagSerializer.errors", new_callable=mocker.PropertyMock)
    expected_errors = "some error"
    errors.return_value = expected_errors

    request = request_builder("POST", reverse("tag-list"))

    response = TagListView().post(request)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == expected_errors
