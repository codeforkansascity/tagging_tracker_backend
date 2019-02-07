from djqscsv import render_to_csv_response
from rest_framework.views import APIView

from common.auth import requires_scope


class CSVView(APIView):

    query = None
    file_name = None
    append_datestamp = True
    scope = None

    @requires_scope(scope)
    def get(self, request):
        return render_to_csv_response(
            queryset=self.query(), filename=self.file_name, append_datestamp=self.append_datestamp
        )
