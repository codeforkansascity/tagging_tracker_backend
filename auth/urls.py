from django.conf.urls import url

from auth.views import get_token

urlpatterns = [
    url(r"^token", get_token, name="token"),
]
