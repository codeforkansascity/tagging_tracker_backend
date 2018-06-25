from django.test import TestCase
from django.http import HttpRequest

from backend.controllers import csv


STATUS_CODES = {"Method Not Allowed": 405}


class TestCSV(TestCase):
    request = HttpRequest()

    def test_csv_address_export__get(self):
        self.request.method = 'GET'
        response = csv.csv_address_export(self.request)
        self.assertEqual(response.getvalue().decode("utf-8-sig"),
                         'ID,point,creator user id,last updated user id,'
                         'neighborhood,street,city,state,zip,owner name,'
                         'owner contact number,owner email,tenant name,'
                         'tenant phone,tenant email,follow up owner needed,'
                         'land bank property,type of property,date updated\r\n')

    def test_csv_address_export__invalid_method(self):
        self.request.method = 'POST'
        response = csv.csv_address_export(self.request)
        self.assert_(response.status_code == STATUS_CODES['Method Not Allowed'])

    def test_csv_tag_export__get(self):
        self.request.method = 'GET'
        response = csv.csv_tag_export(self.request)
        self.assertEqual(response.getvalue().decode("utf-8-sig"),
                         "ID,address_id,creator user id,last updated user id,"
                         "crossed out,date updated,date taken,description,"
                         "gang related,img,neighborhood,racially motivated,"
                         "square footage,surface,tag words,tag initials\r\n")

    def test_csv_tag_export__invalid_method(self):
        self.request.method = 'POST'
        response = csv.csv_tag_export(self.request)
        self.assert_(response.status_code == STATUS_CODES['Method Not Allowed'])
