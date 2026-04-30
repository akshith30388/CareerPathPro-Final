"""
ASGI config for career_platform project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

environment = os.environ.get('ENVIRONMENT', 'local')
if environment == 'production':
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'career_platform.settings.production')
else:
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'career_platform.settings.local')

application = get_asgi_application()
