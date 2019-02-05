from django.conf.urls import url
from backend.controllers import tag
from backend.views.index import index
from backend.views.address import AddressView, AddressListView, AddressTagsView
from backend.views.csv import TagDownloadView, AddressDownloadView

urlpatterns = [
    url(r'^$', index, name="index"),
    url(r'^address/(?P<pk>[0-9]+)/tags/?$', AddressTagsView.as_view(), name="address-tags"),
    url(r'^address/(?P<pk>[0-9]+)/?$', AddressView.as_view(), name="address"),
    url(r'^address/?$', AddressListView().as_view(), name="address-list"),
    url(r'^address/address.csv', AddressDownloadView().as_view(), name="addresses-download"),
    url(r'^tags/?$', tag.tag_list, name="tag-list"),
    url(r'^tags/(?P<pk>[0-9]+)/?$', tag.tag_detail, name="tag"),
    url(r'^tags/tags.csv', TagDownloadView().as_view(), name="tags-download"),
]
