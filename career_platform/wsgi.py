import os

from django.core.wsgi import get_wsgi_application

# Production-first for PythonAnywhere deployment.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

application = get_wsgi_application()
