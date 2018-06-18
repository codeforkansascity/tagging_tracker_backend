from django.http import HttpResponse
from djqscsv import render_to_csv_response
from django.views.decorators.csrf import csrf_exempt
from backend.models import Address, Tag


@csrf_exempt
def csv_address_export(request):
    """
    Allows for the download of the addresses as a .csv file
    :param request:
    :return: a .csv file for download
    """
    response = HttpResponse(status=405)
    if request.method == "GET":
        addresses = Address.objects.all()
        response = render_to_csv_response(queryset=addresses, filename='addresses.csv', append_datestamp=True)
    return response


@csrf_exempt
def csv_tag_export(request):
    """
    Allows for the download of the tags as a .csv file
    :param request:
    :return: a .csv file for download
    """
    response = HttpResponse(status=405)
    if request.method == "GET":
        tags = Tag.objects.all()
        response = render_to_csv_response(queryset=tags, filename='tags.csv', append_datestamp=True)
    return response
