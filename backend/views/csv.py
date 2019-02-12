from backend.models import Address, Tag
from common.views import CSVView


class AddressDownloadView(CSVView):
    query = Address.objects.all
    file_name = "address.csv"
    scopes = {"get": "read:address"}


class TagDownloadView(CSVView):
    query = Tag.objects.all
    file_name = "tags.csv"
    scopes = {"get": "read:tag"}
