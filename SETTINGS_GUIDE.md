# Django Settings Configuration Guide

## Overview

CarrerPathPro uses a modular Django settings architecture that supports multiple environments with ease. The settings are split into:

- **base.py**: Shared configuration for all environments
- **local.py**: Development environment settings
- **production.py**: Production environment settings (PythonAnywhere)

## Settings Structure

```
career_platform/settings/
├── __init__.py
├── base.py          # Shared settings
├── local.py         # Local development
└── production.py    # Production (PythonAnywhere)
```

## How to Select Settings

The correct settings module is automatically selected based on the `ENVIRONMENT` environment variable:

```python
# In manage.py and wsgi.py:
environment = os.environ.get('ENVIRONMENT', 'local')
if environment == 'production':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'career_platform.settings.production')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'career_platform.settings.local')
```

## base.py - Shared Settings

### Installed Apps

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Custom apps
    'users',
    'assessments',
    'appointments',
    'recommendations',
    'chat',
    'dashboard',
]
```

### Middleware

```python
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Static files
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

### Static Files

```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Production collection point
```

### Authentication

```python
AUTH_USER_MODEL = 'users.CustomUser'
LOGIN_URL = '/users/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/users/login/'
```

### Internationalization

```python
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
```

## local.py - Local Development Settings

### Database (SQLite)

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'carrerPathpro.sqlite3',
    }
}
```

### Debug Mode

```python
DEBUG = True  # Enable debug mode
SECRET_KEY = 'django-insecure-local-dev-key'  # Local development key
```

### Static Files

```python
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
```

### Security (Disabled for Local Development)

```python
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
```

### Email Backend

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Console output
```

### Logging

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
```

## production.py - Production Settings (PythonAnywhere)

### Database (MySQL)

```python
# Reads from DATABASE_URL or individual DB_* environment variables
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pathpro_mysql',
        'USER': 'pathpro',
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}
```

### Debug Mode

```python
DEBUG = False  # NEVER True in production
SECRET_KEY = os.environ.get('SECRET_KEY')  # Read from environment
```

### Allowed Hosts

```python
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com', 'www.yourusername.pythonanywhere.com']
```

### Static Files (WhiteNoise)

```python
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Security Features

```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### Email Configuration

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = os.environ.get('EMAIL_PORT', 587)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
```

## Environment Variables

### .env File Format

```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
ENVIRONMENT=production

DATABASE_URL=mysql://user:password@host:port/database
DB_USER=pathpro
DB_PASSWORD=your_db_password
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=pathpro_mysql

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password
DEFAULT_FROM_EMAIL=noreply@carrerpathpro.com
```

### Required Variables

**For All Environments:**
- `ENVIRONMENT`: `local` or `production`

**For Production Only:**
- `SECRET_KEY`: Django secret key (generate with: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- `DEBUG`: `False`
- `ALLOWED_HOSTS`: Your domain(s)
- `DATABASE_URL` or `DB_*` variables
- `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` (for email functionality)

### Optional Variables

- `EMAIL_HOST`: Default: `smtp.gmail.com`
- `EMAIL_PORT`: Default: `587`
- `EMAIL_USE_TLS`: Default: `True`

## Switching Between Environments

### Local Development

```bash
# .env file
ENVIRONMENT=local
DEBUG=True

# Then run:
python manage.py runserver
```

### Production (PythonAnywhere)

```bash
# .env file
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=<unique-key>
ALLOWED_HOSTS=<your-domain>
DATABASE_URL=mysql://...

# Then the app automatically uses production.py
```

## Customizing Settings

### Add New Setting

1. Add to `base.py` if used in all environments
2. Add to specific environment file if environment-specific

Example:

```python
# In base.py
CACHE_TIMEOUT = 3600

# In local.py (override)
CACHE_TIMEOUT = 0  # No caching in development

# In production.py (override)
CACHE_TIMEOUT = 7200  # Longer cache in production
```

### Add New Environment

1. Create `myenv.py` in `career_platform/settings/`
2. Import base: `from .base import *`
3. Override specific settings
4. Update `manage.py` and `wsgi.py`:

```python
environment = os.environ.get('ENVIRONMENT', 'local')
if environment == 'production':
    settings_module = 'career_platform.settings.production'
elif environment == 'myenv':
    settings_module = 'career_platform.settings.myenv'
else:
    settings_module = 'career_platform.settings.local'
```

## Troubleshooting

### Wrong Settings Module Loaded

Check which module is being used:

```bash
python -c "import os; from django.conf import settings; print(os.environ.get('DJANGO_SETTINGS_MODULE'))"
```

### Settings Not Updated

1. Check `.env` file is in project root
2. Ensure `ENVIRONMENT` variable is set
3. Reload web app if in production
4. Check error logs

### Database Connection Error

1. Verify `DATABASE_URL` or individual `DB_*` variables
2. Test connection: `python manage.py dbshell`
3. Check database credentials in `.env`

### Static Files Not Loading

1. Run: `python manage.py collectstatic --noinput`
2. Check `STATIC_ROOT` path is correct
3. In production, verify static file mapping in web app config

## Best Practices

1. **Never commit `.env`** - Use `.env.example` template
2. **Use environment variables** - Don't hardcode secrets
3. **Test before deployment** - Run tests in local environment
4. **Keep secrets secure** - Use strong, unique SECRET_KEY
5. **Document changes** - Update `.env.example` when adding new variables
6. **Separate concerns** - Keep environment-specific settings separate
7. **Use DEBUG flag** - Always False in production
8. **Enable HTTPS** - Always in production

## Security Checklist

- [ ] SECRET_KEY is unique and strong
- [ ] DEBUG is False in production
- [ ] ALLOWED_HOSTS is specific (not `*`)
- [ ] DATABASE password is secure
- [ ] .env is in .gitignore
- [ ] HTTPS is enforced
- [ ] Email credentials are app-specific (not main password)
- [ ] Superuser has strong password
- [ ] Settings are not in version control

---

For more information, see:
- [Django Settings Documentation](https://docs.djangoproject.com/en/6.0/topics/settings/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/)
