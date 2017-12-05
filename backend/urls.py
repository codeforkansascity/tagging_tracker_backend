from django.conf.urls import url
from backend import views

urlpatterns = [
    url(r'^address/$', views.address_list),
    url(r'^tags/$', views.tag_list),
    url(r'^tags/(?P<pk>[0-9]+)/$', views.tag_detail)
]