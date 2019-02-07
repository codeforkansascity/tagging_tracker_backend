from backend.models import Address, Tag
from backend.views.csv import AddressDownloadView, TagDownloadView


def test_address_download_view():
    view = AddressDownloadView()

    assert view.query == Address.objects.all
    assert view.file_name == "address.csv"
    assert view.scopes == {"get": "read:address"}


def test_tag_download_view():
    view = TagDownloadView()

    assert view.query == Tag.objects.all
    assert view.file_name == "tags.csv"
    assert view.scopes == {"get": "read:tag"}
