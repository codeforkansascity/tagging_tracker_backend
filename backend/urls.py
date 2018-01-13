from django.conf.urls import url
from backend import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^index/$', views.index),
    url(r'^address/(?P<pk>[0-9]+)/tags/$', views.address_tags),
    url(r'^address/(?P<pk>[0-9]+)/$', views.address_detail),
    url(r'^address/$', views.address_list),
    url(r'^address/(?P<pk>[0-9]+)/$', views.address_detail),
    url(r'^tags/$', views.tag_list),
    url(r'^tags/(?P<pk>[0-9]+)/$', views.tag_detail),
    url(r'^address/address.csv', views.csv_address_export),
]