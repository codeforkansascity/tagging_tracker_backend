"""
WSGI config for tagging_tracker project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import dotenv

from django.core.wsgi import get_wsgi_application

dotenv.load_dotenv(os.path.join(os.path.dirname(__name__), "local.env"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tagging_tracker.settings")

application = get_wsgi_application()
