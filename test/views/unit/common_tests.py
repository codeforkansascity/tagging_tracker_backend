import pytest

from common.views import CSVView, BaseView


def test_base_view_check_permissions_returns_none_if_auth_disabled(mocker):
    assert BaseView().check_permissions(mocker.Mock()) is None


@pytest.mark.usefixtures("enable_auth")
def test_base_view_check_permissions_returns_none_if_no_scope_found(request_builder):
    request = request_builder("get", "/some/endpoint")

    assert BaseView().check_permissions(request) is None


@pytest.mark.usefixtures("enable_auth")
def test_base_view_returns_none_if_has_valid_scope_is_true(request_builder, mocker):
    has_valid_scope = mocker.patch("common.views.has_valid_scope")
    has_valid_scope.return_value = True
    request = request_builder("get", "/some/endpoint")

    view = BaseView()
    view.scopes = {"get": "some:scope"}

    response = view.check_permissions(request)
    assert response is None
    has_valid_scope.assert_called_once_with(request, "some:scope")


@pytest.mark.usefixtures("enable_auth")
def test_base_view_raises_permissions_error_if_has_valid_scope_is_false(request_builder, mocker):
    has_valid_scope = mocker.patch("common.views.has_valid_scope")
    has_valid_scope.return_value = False
    request = request_builder("get", "/some/endpoint")

    view = BaseView()
    view.scopes = {"get": "some:scope"}

    with pytest.raises(PermissionError):
        view.check_permissions(request)
    has_valid_scope.assert_called_once_with(request, "some:scope")


def test_csv_view(mocker):
    view = CSVView()
    query = mocker.Mock()
    file_name = "file name"
    view.query = query
    view.file_name = file_name

    csv_render = mocker.patch("common.views.render_to_csv_response")

    response = view.get(mocker.Mock())

    assert view.append_datestamp is True
    assert response == csv_render.return_value
    csv_render.assert_called_once_with(
        queryset=query.return_value,
        filename=file_name,
        append_datestamp=view.append_datestamp
    )
