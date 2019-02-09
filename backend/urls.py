from django.conf.urls import url

from backend.views.contacts import ContactListView, ContactTypesView
from backend.views.index import index
from backend.views.address import AddressView, AddressListView, AddressTagsView
from backend.views.tag import TagView, TagListView
from backend.views.csv import TagDownloadView, AddressDownloadView

urlpatterns = [
    url(r'^$', index, name="index"),
    url(r'^address/?$', AddressListView.as_view(), name="address-list"),
    url(r'^address/(?P<pk>[0-9]+)/?$', AddressView.as_view(), name="address"),
    url(r'^address/(?P<pk>[0-9]+)/tags/?$', AddressTagsView.as_view(), name="address-tags"),
    url(r'^address/(?P<pk>[0-9]+)/contacts', ContactListView.as_view(), name="address-contacts"),
    url(r'^address/address.csv', AddressDownloadView.as_view(), name="addresses-download"),
    url(r'^contact-types', ContactTypesView.as_view(), name="contact-types"),
    url(r'^tags/?$', TagListView.as_view(), name="tag-list"),
    url(r'^tags/(?P<pk>[0-9]+)/?$', TagView.as_view(), name="tag"),
    url(r'^tags/tags.csv', TagDownloadView.as_view(), name="tags-download"),
]
