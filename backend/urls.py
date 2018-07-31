from django.conf.urls import url
from backend.controllers import address, csv, index, tag

urlpatterns = [
    url(r'^$', index.index),
    url(r'^index/?$', index.index),
    url(r'^address/(?P<pk>[0-9]+)/tags/?$', address.address_tags),
    url(r'^address/(?P<pk>[0-9]+)/?$', address.address_detail),
    url(r'^address/?$', address.address_list),
    url(r'^address/(?P<pk>[0-9]+)/?$', address.address_detail),
    url(r'^address/address.csv', csv.csv_address_export),
    url(r'^tags/?$', tag.tag_list),
    url(r'^tags/(?P<pk>[0-9]+)/?$', tag.tag_detail),
    url(r'^tags/tags.csv', csv.csv_tag_export),
]
