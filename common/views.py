import logging

from django.conf import settings
from djqscsv import render_to_csv_response
from rest_framework.views import APIView

from common.auth import requires_scope, has_valid_scope


logger = logging.getLogger(__name__)


class BaseView(APIView):
    scopes = {}

    def check_permissions(self, request):
        if settings.DISABLE_AUTH:
            logger.debug("auth disabled scope check skipped")
            return True

        scope = self.scopes.get(request.method.lower())
        if scope is None:
            return True

        return has_valid_scope(request, scope)


class CSVView(BaseView):

    query = None
    file_name = None
    append_datestamp = True

    def get(self, request):
        return render_to_csv_response(
            queryset=self.query(), filename=self.file_name, append_datestamp=self.append_datestamp
        )
