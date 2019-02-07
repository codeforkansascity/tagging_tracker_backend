import os
from functools import wraps

import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response

# This entire module was taken from https://bit.ly/2t8LZVD
from rest_framework.views import APIView


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


def requires_scope(required_scope):
    """Determines if the required scope is present in the access token
    Args:
        required_scope (str): The scope required to access the resource
    """
    def require_scope(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if settings.DISABLE_AUTH:
                return f(*args, **kwargs)

            request = args[1] if isinstance(args[0], APIView) else args[0]
            token = get_token_auth_header(request)

            decoded = jwt.decode(
                token, settings.PUBLIC_KEY, audience=os.environ["AUTH0_AUDIENCE"], algorithms=["RS256"]
            )

            if decoded.get("scope"):
                token_scopes = decoded["scope"].split()
                if required_scope in token_scopes:
                    return f(*args, **kwargs)

            return Response(
                {"message": "You do not have access to this resource"}, status=status.HTTP_403_FORBIDDEN
            )
        return decorated
    return require_scope
