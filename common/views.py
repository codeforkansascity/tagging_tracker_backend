import logging

from django.conf import settings
from djqscsv import render_to_csv_response
from rest_framework.views import APIView

from common.auth import has_valid_scope


logger = logging.getLogger(__name__)


class BaseView(APIView):
    scopes = {}

    def check_permissions(self, request):
        if settings.DISABLE_AUTH:
            logger.debug("auth disabled scope check skipped")
            return

        scope = self.scopes.get(request.method.lower())
        if scope is None:
            return

        if not has_valid_scope(request, scope):
            raise PermissionError
        return super().check_permissions(request)


class CSVView(BaseView):

    query = None
    file_name = None
    append_datestamp = True

    def get(self, request):
        return render_to_csv_response(
            queryset=self.query(), filename=self.file_name, append_datestamp=self.append_datestamp
        )
