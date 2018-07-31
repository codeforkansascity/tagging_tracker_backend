from django.conf.urls import url
from backend.controllers.address import AddressResource
from backend.controllers.csv import CSVResource
from backend.controllers.index import IndexResource
from backend.controllers.tag import TagResource

urlpatterns = [
    url(r'^$', IndexResource.index),
    url(r'^index/?$', IndexResource.index),
    url(r'^address/(?P<pk>[0-9]+)/tags/?$', AddressResource.address_tags),
    url(r'^address/(?P<pk>[0-9]+)/?$', AddressResource.address_detail),
    url(r'^address/?$', AddressResource.address_list),
    url(r'^address/(?P<pk>[0-9]+)/?$', AddressResource.address_detail),
    url(r'^address/address.csv', CSVResource.csv_address_export),
    url(r'^tags/?$', TagResource.tag_list),
    url(r'^tags/(?P<pk>[0-9]+)/?$', TagResource.tag_detail),
    url(r'^tags/tags.csv', CSVResource.csv_tag_export),
]
