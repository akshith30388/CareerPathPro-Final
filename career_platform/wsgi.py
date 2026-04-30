"""
WSGI config for CarrerPathPro on PythonAnywhere.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application

# Add the project directory to the path
project_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_dir))

# Determine environment and set Django settings module
environment = os.environ.get('ENVIRONMENT', 'local')
if environment == 'production':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'career_platform.settings.production')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'career_platform.settings.local')

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    env_file = project_dir / '.env'
    if env_file.exists():
        load_dotenv(env_file)
except ImportError:
    pass

application = get_wsgi_application()
