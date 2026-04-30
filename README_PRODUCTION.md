# CarrerPathPro - Django Career Platform

A comprehensive Django application for career assessment, planning, and guidance. Built with production-ready configuration for PythonAnywhere deployment.

## Features

- **Career Assessment**: Multi-category assessment (Aptitude, Interest, Personality)
- **Personalized Recommendations**: AI-powered career path suggestions
- **Appointment Management**: Book counseling sessions with career advisors
- **Chat System**: Real-time communication with counselors
- **Resume Builder**: Create and manage professional resumes
- **Dashboard**: Student and counselor views with analytics
- **User Management**: Secure authentication and role-based access

## Project Structure

```
CarrerPathPro/
├── career_platform/          # Main Django project
│   ├── settings/
│   │   ├── base.py          # Base settings (shared)
│   │   ├── local.py         # Local development settings
│   │   ├── production.py    # Production settings (PythonAnywhere)
│   │   └── __init__.py
│   ├── urls.py
│   ├── wsgi.py              # WSGI configuration for PythonAnywhere
│   └── asgi.py
├── users/                    # User management app
├── assessments/              # Career assessment app
├── appointments/             # Appointment booking app
├── recommendations/          # Career recommendations app
├── chat/                     # Chat system app
├── dashboard/                # Dashboard views
├── templates/                # HTML templates
├── static/                   # CSS, JS, images
├── media/                    # User-uploaded files
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## Installation & Setup

### Prerequisites

- Python 3.9+
- pip (Python package manager)
- MySQL Server (for production)
- Virtual environment tool (venv or virtualenv)

### Local Development Setup

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd CarrerPathPro
```

#### 2. Create Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Create Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your local settings
# For local development, you can use SQLite (default in local.py)
```

#### 5. Apply Migrations

```bash
# Migrate to latest database schema
python manage.py migrate

# Create superuser for admin panel
python manage.py createsuperuser
```

#### 6. Load Sample Data (Optional)

```bash
# Load career assessment questions
python manage.py seed_assessment_questions
```

#### 7. Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## Deployment to PythonAnywhere

### Prerequisites on PythonAnywhere

1. **PythonAnywhere Account**: Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. **MySQL Database**: Created in PythonAnywhere MySQL tab
3. **Web App**: Created with Django framework

### Step-by-Step Deployment

#### 1. Create MySQL Database

1. Log in to PythonAnywhere
2. Go to **Databases** tab
3. Create a new MySQL database: `pathpro_mysql`
4. Note the database credentials

#### 2. Clone Repository to PythonAnywhere

1. Go to **Consoles** → **Bash**
2. Clone your repository:

```bash
cd ~
git clone <repository-url>
cd CarrerPathPro
```

#### 3. Create Virtual Environment

```bash
mkvirtualenv --python=/usr/bin/python3.10 carrer
pip install -r requirements.txt
```

#### 4. Configure .env File

```bash
# In PythonAnywhere console
nano .env
```

Add the following (replace with your actual values):

```env
SECRET_KEY=generate-a-new-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourusername.pythonanywhere.com
ENVIRONMENT=production

DATABASE_URL=mysql://pathpro:your_db_password@127.0.0.1:3306/pathpro_mysql
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

**Generate SECRET_KEY:**

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### 5. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

#### 6. Run Migrations

```bash
python manage.py migrate
python manage.py seed_assessment_questions
```

#### 7. Create Superuser

```bash
python manage.py createsuperuser
```

#### 8. Configure Web App

1. Go to **Web** tab
2. Click your web app
3. Go to **Code** section
4. Set **WSGI configuration file** to:
   ```
   /home/yourusername/CarrerPathPro/career_platform/wsgi.py
   ```

5. **Source code** should be:
   ```
   /home/yourusername/CarrerPathPro
   ```

6. **Working directory** should be:
   ```
   /home/yourusername/CarrerPathPro
   ```

#### 9. Configure Virtualenv

1. In **Virtualenv** section, set to:
   ```
   /home/yourusername/.virtualenvs/carrer
   ```

#### 10. Add to WSGI Config

Go to Web tab → WSGI configuration file and add at the top (before the existing content):

```python
import os
import sys

path = '/home/yourusername/CarrerPathPro'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'career_platform.settings.production'
```

#### 11. Reload Web App

Click the **Reload** button in the **Web** tab to apply changes.

### Troubleshooting PythonAnywhere Deployment

#### 1. Check Error Log

```bash
cat /var/log/yourusername.pythonanywhere.com.error.log
```

#### 2. Check Server Log

In PythonAnywhere Web tab, click **Server log** link.

#### 3. Database Connection Issues

```bash
# Test MySQL connection
mysql -u pathpro -p -h 127.0.0.1 pathpro_mysql
```

#### 4. Static Files Not Loading

```bash
# Recreate static files
python manage.py collectstatic --clear --noinput
```

#### 5. Permission Issues

```bash
chmod +x manage.py
```

## Environment Variables Configuration

### Local Development (.env)

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
ENVIRONMENT=local
```

### Production (.env on PythonAnywhere)

```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourusername.pythonanywhere.com
ENVIRONMENT=production
DATABASE_URL=mysql://user:password@host:port/database
```

## Settings Architecture

The project uses a modular settings approach:

- **base.py**: Common settings for all environments
- **local.py**: Development settings (SQLite, DEBUG=True)
- **production.py**: Production settings (MySQL, HTTPS, etc.)

### Switching Settings

The settings module is selected based on the `ENVIRONMENT` variable:

```python
if environment == 'production':
    settings = 'career_platform.settings.production'
else:
    settings = 'career_platform.settings.local'
```

## Database

### Local Development

SQLite database (automatic):
```
carrerPathpro.sqlite3
```

### Production (PythonAnywhere)

MySQL database configuration in `production.py`:
- **Host**: 127.0.0.1
- **Database**: pathpro_mysql
- **User**: pathpro
- **Port**: 3306

## Static Files

- **Local**: Served directly by Django
- **Production**: Collected to `staticfiles/` directory and served by WhiteNoise

### Collecting Static Files

```bash
python manage.py collectstatic
```

## Security Considerations

### Production Security Features

1. **HTTPS Enforcement**: `SECURE_SSL_REDIRECT = True`
2. **HSTS**: HTTP Strict Transport Security enabled
3. **Secure Cookies**: `SESSION_COOKIE_SECURE = True`
4. **CSRF Protection**: Built-in Django CSRF middleware
5. **XSS Prevention**: Security middleware enabled
6. **Content Security Policy**: Configured in `base.py`

### Best Practices

1. **SECRET_KEY**: Keep this secret! Generate a new one for production:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

2. **DEBUG**: Always set to `False` in production

3. **ALLOWED_HOSTS**: Specify exact domains, never use `*` in production

4. **Database Password**: Use strong passwords and store in `.env`

5. **Email Credentials**: Use app-specific passwords (especially for Gmail)

## Maintenance

### Regular Tasks

#### 1. Database Backups

```bash
# Backup MySQL database
mysqldump -u pathpro -p pathpro_mysql > backup.sql
```

#### 2. Check Logs

```bash
# Application logs
tail -f logs/django.log
```

#### 3. Update Dependencies

```bash
pip install --upgrade -r requirements.txt
```

#### 4. Run Migrations After Update

```bash
python manage.py migrate
```

## API Documentation

### Authentication

All endpoints require user authentication. Log in at `/users/login/`

### Main Endpoints

- `/assessments/` - Career assessment
- `/dashboard/` - Dashboard
- `/appointments/` - Appointment management
- `/recommendations/` - Career recommendations
- `/chat/` - Communication
- `/admin/` - Admin panel (superuser only)

## Contributing

1. Create a new branch: `git checkout -b feature-name`
2. Make your changes
3. Commit: `git commit -m "Add feature"`
4. Push: `git push origin feature-name`
5. Create Pull Request

## Support

For issues and questions:
1. Check the [troubleshooting section](#troubleshooting-pythonanywhere-deployment)
2. Review PythonAnywhere [help documentation](https://help.pythonanywhere.com)
3. Contact the development team

## License

[Add your license here]

## Changelog

### Version 1.0.0 (Current)
- Initial production setup
- Assessment system with mock data
- Career recommendations engine
- User authentication system
- Appointment booking system

---

**Last Updated**: April 30, 2026  
**Environment**: Django 6.0.1 | Python 3.9+  
**Deployment**: PythonAnywhere
