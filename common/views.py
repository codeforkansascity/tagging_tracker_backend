from djqscsv import render_to_csv_response
from rest_framework.views import APIView


class CSVView(APIView):

    query = None
    file_name = None
    append_datestamp = True

    def get(self, request):
        return render_to_csv_response(
            queryset=self.query(), filename=self.file_name, append_datestamp=self.append_datestamp
        )
