import logging

from django.conf import settings
from djqscsv import render_to_csv_response
from rest_framework.views import APIView

from common.auth import has_valid_scope


logger = logging.getLogger(__name__)


class BaseView(APIView):
    """
    Handles Auth0 authentication scope authentication for endpoints.
    Authentication can be disabled via DISABLE_AUTH=1 in envars.
    If scope is not defined for method on view the check is not made.

    Define 'scopes' as follows
    scopes = {
        "method_name_in_lower_case": "auth0scope"
    }
    """

    scopes = {}

    def check_permissions(self, request):
        if settings.DISABLE_AUTH:
            logger.debug("auth disabled scope check skipped")
            return

        scope = self.scopes.get(request.method.lower())
        if scope is None:
            return

        valid_scope, msg = has_valid_scope(request, scope)
        if not valid_scope:
            logger.debug(f"Invalid permissions: {msg}")
            raise PermissionError
        return super().check_permissions(request)


class CSVView(BaseView):
    """
    View that translates callable query into CSV download.

    query - Should be a queryset that can be invoked
    file_name - Name of download w/o .csv as it is automatically appended
    append_timestamp - will automatically append the timestamp of the download to file_name if True

    class MyDownload(CSVView):
        query = MyModel.objects.all  # note the lack of invocation
        file_name = "my-model-data"
    """

    query = None
    file_name = None
    append_datestamp = True

    def get(self, request):
        return render_to_csv_response(
            queryset=self.query(),
            filename=self.file_name,
            append_datestamp=self.append_datestamp,
        )
