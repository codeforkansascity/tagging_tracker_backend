from django.conf.urls import url
from backend.controllers import address_controller, csv_controller, index_controller, tag_controller

urlpatterns = [
    url(r'^$', index_controller.index),
    url(r'^index/?$', index_controller.index),
    url(r'^address/(?P<pk>[0-9]+)/tags/?$', address_controller.address_tags),
    url(r'^address/(?P<pk>[0-9]+)/?$', address_controller.address_detail),
    url(r'^address/?$', address_controller.address_list),
    url(r'^address/(?P<pk>[0-9]+)/?$', address_controller.address_detail),
    url(r'^address/address.csv', csv_controller.csv_address_export),
    url(r'^tags/?$', tag_controller.tag_list),
    url(r'^tags/(?P<pk>[0-9]+)/?$', tag_controller.tag_detail),
    url(r'^tags/tags.csv', csv_controller.csv_tag_export),
]
