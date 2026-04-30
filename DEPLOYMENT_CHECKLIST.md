# PythonAnywhere Deployment Checklist

## Pre-Deployment (Local Environment)

- [ ] Update `requirements.txt` with all dependencies
- [ ] Test locally: `python manage.py runserver`
- [ ] Run migrations locally: `python manage.py migrate`
- [ ] Collect static files locally: `python manage.py collectstatic --noinput`
- [ ] Run tests (if available): `python manage.py test`
- [ ] Check for any hardcoded secrets or passwords
- [ ] Update `.env.example` with all required variables
- [ ] Commit all changes to git: `git add . && git commit -m "Pre-production deployment"`
- [ ] Push to repository: `git push origin main`

## PythonAnywhere Setup

### Step 1: Create Database
- [ ] Log in to PythonAnywhere
- [ ] Go to **Databases** tab
- [ ] Create new MySQL database: `pathpro_mysql`
- [ ] Note username, password, and host (usually 127.0.0.1)
- [ ] Record connection string

### Step 2: Create Web App
- [ ] Go to **Web** tab
- [ ] Click **Add a new web app**
- [ ] Choose **Manual configuration** (not from template)
- [ ] Select **Python 3.10** (or latest available)
- [ ] Note the username and domain

### Step 3: Clone Repository
- [ ] Open **Bash console**
- [ ] Navigate to home: `cd ~`
- [ ] Clone repository: `git clone <repo-url>`
- [ ] Navigate to project: `cd CarrerPathPro`

### Step 4: Set Up Virtual Environment
- [ ] Create virtualenv: `mkvirtualenv --python=/usr/bin/python3.10 carrer`
- [ ] Verify activation: `which python`
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Verify Django installed: `django-admin --version`

### Step 5: Configure Environment
- [ ] Copy template: `cp .env.example .env`
- [ ] Edit .env: `nano .env`
- [ ] Set SECRET_KEY: Generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- [ ] Set ALLOWED_HOSTS: `yourusername.pythonanywhere.com`
- [ ] Set DATABASE_URL with actual credentials
- [ ] Set ENVIRONMENT: `production`
- [ ] Save file (Ctrl+X, Y, Enter)

### Step 6: Initialize Database
- [ ] Run migrations: `python manage.py migrate`
- [ ] Create superuser: `python manage.py createsuperuser`
- [ ] Load sample data: `python manage.py seed_assessment_questions`
- [ ] Collect static files: `python manage.py collectstatic --noinput --clear`

### Step 7: Configure Web App
- [ ] Go to **Web** tab
- [ ] Click your web app
- [ ] Go to **Code** section:
  - [ ] Source code: `/home/yourusername/CarrerPathPro`
  - [ ] Working directory: `/home/yourusername/CarrerPathPro`
  
- [ ] Go to **Virtualenv** section:
  - [ ] Set to: `/home/yourusername/.virtualenvs/carrer`

- [ ] Go to **WSGI configuration file**:
  - [ ] Click the filename link to edit
  - [ ] Paste content from `career_platform/wsgi_pythonanywhere.py`
  - [ ] Replace `yourusername` with actual username
  - [ ] Save file

- [ ] Go to **Web Security**:
  - [ ] Force HTTPS: ON
  - [ ] HSTS enabled: ON

### Step 8: Configure Static Files
- [ ] Go to **Web** tab
- [ ] Click your web app
- [ ] Scroll to **Static files** section
- [ ] Add static file mapping:
  - [ ] URL: `/static/`
  - [ ] Directory: `/home/yourusername/CarrerPathPro/staticfiles`
- [ ] Add media file mapping (optional):
  - [ ] URL: `/media/`
  - [ ] Directory: `/home/yourusername/CarrerPathPro/media`

### Step 9: Reload Application
- [ ] Click **Reload** button in Web tab
- [ ] Wait for 10-20 seconds
- [ ] Go to your domain: `https://yourusername.pythonanywhere.com`

## Post-Deployment Verification

- [ ] Access homepage: Should load without errors
- [ ] Check static files: CSS/JS should load correctly
- [ ] Admin panel: Can access `/admin/` with superuser
- [ ] Check error log: `/var/log/yourusername.pythonanywhere.com.error.log`
- [ ] Database connection: Can access assessments page
- [ ] Create test user: Can register and login
- [ ] Assessment works: Can start and complete assessment
- [ ] HTTPS working: Should redirect HTTP to HTTPS

## Monitoring & Maintenance

### Daily
- [ ] Check error log for any new errors
- [ ] Monitor application performance

### Weekly
- [ ] Check database size
- [ ] Verify backups are working
- [ ] Review user feedback/issues

### Monthly
- [ ] Update dependencies: `pip install --upgrade -r requirements.txt`
- [ ] Run database maintenance
- [ ] Review and optimize slow queries
- [ ] Update Django security patches

## Troubleshooting

### Web App Not Starting
```bash
# Check error log
cat /var/log/yourusername.pythonanywhere.com.error.log

# Check WSGI configuration
# Verify path is correct in Web tab

# Reload web app
# Click Reload button in Web tab
```

### Database Connection Error
```bash
# Check MySQL is running
mysql -u username -p -h 127.0.0.1

# Verify .env file has correct credentials
cat .env

# Test connection manually
python manage.py dbshell
```

### Static Files Not Loading
```bash
# Recreate static files
python manage.py collectstatic --clear --noinput

# Verify static file mapping in Web tab
# URL should be /static/
# Directory should end with /staticfiles
```

### Import Errors
```bash
# Ensure virtual environment is active
source ~/.virtualenvs/carrer/bin/activate

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Check Python path
python -c "import sys; print(sys.path)"
```

## Rollback Plan

If deployment fails or breaks production:

1. **Stop Web App** (in Web tab)
2. **Check Error Log** for specific error
3. **Git Revert** if code was the issue:
   ```bash
   git log  # Find previous commit
   git revert <commit-hash>
   ```
4. **Fix Issue Locally**
5. **Push Fix** to repository
6. **Pull Changes** on PythonAnywhere:
   ```bash
   git pull origin main
   ```
7. **Run Migrations** if needed
8. **Collect Static** files again
9. **Reload Web App**

## Security Checklist

- [ ] SECRET_KEY is unique and strong
- [ ] DEBUG is False in production
- [ ] ALLOWED_HOSTS does not contain `*`
- [ ] DATABASE_URL is secure (strong password)
- [ ] .env file is in .gitignore
- [ ] Email credentials are app-specific passwords
- [ ] HTTPS is enforced (Force HTTPS ON)
- [ ] HSTS headers are enabled
- [ ] Superuser account has strong password
- [ ] Regular security updates applied

## Notes

- Project name: **CarrerPathPro**
- Django project: **career_platform**
- Database: **pathpro_mysql**
- Python version: **3.10+**
- Virtual env: **carrer**

---

**Deployment Date**: [Date of deployment]  
**Deployed By**: [Your name]  
**Version**: [Version number]
