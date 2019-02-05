from common.views import CSVView


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
