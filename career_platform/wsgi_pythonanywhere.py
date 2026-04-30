"""
PythonAnywhere WSGI Configuration File

This file should be placed at: /home/yourusername/CarrerPathPro/career_platform/wsgi.py

For PythonAnywhere, update the Web tab:
1. WSGI configuration file path: /home/yourusername/CarrerPathPro/career_platform/wsgi.py
2. Source code: /home/yourusername/CarrerPathPro
3. Working directory: /home/yourusername/CarrerPathPro
4. Virtualenv: /home/yourusername/.virtualenvs/carrer

Instructions:
1. Go to Web tab in PythonAnywhere
2. Click on your web app
3. In "Code" section, set WSGI configuration file to path above
4. If using a custom WSGI file, click the filename link to edit it
5. Replace content with the code below
"""

import os
import sys
from pathlib import Path

# Add project directory to path
project_dir = '/home/yourusername/CarrerPathPro'
sys.path.insert(0, project_dir)

# Set environment
os.environ['ENVIRONMENT'] = 'production'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

# Load environment variables from .env
env_file = Path(project_dir) / '.env'
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    os.environ.setdefault(key, value)

# Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
