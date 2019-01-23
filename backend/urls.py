from django.conf.urls import url
from backend.controllers import address, csv, index, tag
from backend.views.address import AddressView

urlpatterns = [
    url(r'^$', index.index),
    url(r'^index/?$', index.index),
    url(r'^address/(?P<pk>[0-9]+)/tags/?$', address.address_tags, name="address-tags"),
    url(r'^address/(?P<pk>[0-9]+)/?$', AddressView.as_view(), name="address"),
    url(r'^address/?$', address.address_list, name="address-list"),
    url(r'^address/address.csv', csv.csv_address_export, name="addresses-download"),
    url(r'^tags/?$', tag.tag_list, name="tag-list"),
    url(r'^tags/(?P<pk>[0-9]+)/?$', tag.tag_detail, name="tag"),
    url(r'^tags/tags.csv', csv.csv_tag_export, name="tags-download"),
]
