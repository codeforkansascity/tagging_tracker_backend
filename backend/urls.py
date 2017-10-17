from django.conf.urls import url
from backend import views

urlpatterns = [
    url(r'^taggingpoints/$', views.taggingpoint_list),
    url(r'^taggingpoints/(?P<pk>[0-9]+)/$', views.taggingpoint_detail)
]