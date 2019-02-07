import os

import jwt
from django.conf import settings
from django.contrib.auth import authenticate

# This module was base off of https://bit.ly/2t8LZVD


def jwt_get_username_from_payload_handler(payload):
    username = payload.get('sub').replace('|', '.')
    authenticate(remote_user=username)
    return username


def get_token_auth_header(request):
    """Obtains the access token from the Authorization Header
    """
    auth = request.META.get("HTTP_AUTHORIZATION", None)
    parts = auth.split()
    token = parts[1]

    return token


def has_valid_scope(request, required_scope):
    token = get_token_auth_header(request)

    decoded = jwt.decode(
        token, settings.PUBLIC_KEY, audience=os.environ["AUTH0_AUDIENCE"], algorithms=["RS256"]
    )

    if decoded.get("scope"):
        token_scopes = decoded["scope"].split()
        return required_scope in token_scopes
    return False
