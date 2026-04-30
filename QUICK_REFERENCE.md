# CarrerPathPro - Quick Reference Card

## 🚀 Local Setup (One Command)

### Windows
```cmd
setup_local.bat
```

### Linux/Mac
```bash
chmod +x setup_local.sh && ./setup_local.sh
```

---

## 📦 Project Info

| Item | Value |
|------|-------|
| **Project Name** | CarrerPathPro |
| **Django Project** | career_platform |
| **Database (Prod)** | pathpro_mysql |
| **Database User** | pathpro |
| **Python Version** | 3.9+ |
| **Framework** | Django 6.0.1 |

---

## 🔧 Essential Commands

```bash
# Setup
python -m venv venv
pip install -r requirements.txt

# Development
python manage.py runserver                  # Start server
python manage.py migrate                    # Apply migrations
python manage.py makemigrations             # Create migrations
python manage.py createsuperuser            # Create admin user
python manage.py seed_assessment_questions  # Load sample data

# Production
python manage.py collectstatic --noinput    # Collect static files
python manage.py migrate                    # Apply migrations

# Testing
python manage.py test                       # Run tests
python manage.py dbshell                    # Database shell
```

---

## 🌍 URLs

| URL | Purpose |
|-----|---------|
| `http://127.0.0.1:8000/` | Homepage (local) |
| `http://127.0.0.1:8000/admin/` | Admin panel |
| `http://127.0.0.1:8000/assessments/` | Career assessment |
| `http://127.0.0.1:8000/dashboard/` | Dashboard |
| `https://yourusername.pythonanywhere.com` | Production |

---

## 📝 Environment Variables

### Local `.env`
```env
ENVIRONMENT=local
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

### Production `.env`
```env
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=<your-secret-key>
ALLOWED_HOSTS=yourusername.pythonanywhere.com
DATABASE_URL=mysql://pathpro:password@127.0.0.1:3306/pathpro_mysql
```

### Generate SECRET_KEY
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | `pip install -r requirements.txt` |
| `Database error` | `python manage.py migrate` |
| `Static files missing` | `python manage.py collectstatic --clear --noinput` |
| `Port already in use` | `python manage.py runserver 8001` |
| `.env not loading` | Check file location in project root |

---

## 📂 Important Files

| File | Purpose |
|------|---------|
| `career_platform/settings/base.py` | Shared settings |
| `career_platform/settings/local.py` | Dev settings |
| `career_platform/settings/production.py` | Prod settings |
| `career_platform/wsgi.py` | WSGI app |
| `requirements.txt` | Dependencies |
| `.env` | Environment variables |
| `.gitignore` | Git ignore rules |

---

## 🔐 Security Checklist

- [ ] SECRET_KEY is unique and strong
- [ ] DEBUG=False in production
- [ ] ALLOWED_HOSTS set correctly
- [ ] .env is in .gitignore
- [ ] Database password is strong
- [ ] HTTPS is enabled (production)
- [ ] Email credentials are app-specific

---

## 📚 Documentation

- `README_PRODUCTION.md` - Full deployment guide
- `DEPLOYMENT_CHECKLIST.md` - Step-by-step checklist
- `SETTINGS_GUIDE.md` - Settings explanation
- `SETUP_SUMMARY.md` - Complete setup overview

---

## 🎯 PythonAnywhere Deployment Steps

1. **Create Database**: `pathpro_mysql`
2. **Clone Repo**: `git clone <url>`
3. **Virtual Env**: `mkvirtualenv --python=/usr/bin/python3.10 carrer`
4. **Install**: `pip install -r requirements.txt`
5. **Configure .env**: Copy and update `.env.example`
6. **Migrate**: `python manage.py migrate`
7. **Static**: `python manage.py collectstatic --noinput`
8. **WSGI**: Point to `/home/username/CarrerPathPro/career_platform/wsgi.py`
9. **Reload**: Click Reload button

---

## 💾 Backup Commands

```bash
# Backup database (MySQL)
mysqldump -u pathpro -p pathpro_mysql > backup.sql

# Backup project
tar -czf carrerpathpro-backup.tar.gz CarrerPathPro/

# Restore database
mysql -u pathpro -p pathpro_mysql < backup.sql
```

---

## 📊 Settings by Environment

| Setting | Local | Production |
|---------|-------|-----------|
| `DEBUG` | True | False |
| `Database` | SQLite | MySQL |
| `HTTPS` | No | Yes |
| `Static` | Django | WhiteNoise |
| `Email` | Console | SMTP |

---

## 🔗 Key Endpoints

```
/users/login/          - Login page
/users/register/       - Registration
/assessments/          - Assessment start
/assessments/take/     - Take assessment
/assessments/result/<id>/  - View result
/dashboard/            - Dashboard
/admin/                - Admin panel
```

---

## 🛠️ Database

### Local (SQLite)
File: `carrerPathpro.sqlite3`

### Production (MySQL)
- **Host**: 127.0.0.1
- **Port**: 3306
- **Name**: pathpro_mysql
- **User**: pathpro

### Connection String (MySQL)
```
mysql://pathpro:password@127.0.0.1:3306/pathpro_mysql
```

---

## 📞 Quick Help

**Nothing working?**
1. Check `.env` file exists and is configured
2. Run migrations: `python manage.py migrate`
3. Check error logs in console
4. Review README_PRODUCTION.md

**Forgot command?**
- See SETUP_SUMMARY.md for full reference

**Settings confused?**
- See SETTINGS_GUIDE.md for detailed explanation

---

## ✅ Verification Checklist

After setup, verify:

- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip list`)
- [ ] .env file created and configured
- [ ] Migrations applied (`python manage.py migrate`)
- [ ] Superuser created
- [ ] Server starts (`python manage.py runserver`)
- [ ] Homepage loads (http://127.0.0.1:8000/)
- [ ] Admin page loads (http://127.0.0.1:8000/admin/)
- [ ] Can login with superuser
- [ ] Assessment page loads
- [ ] Static files load (CSS/JS visible)

---

**Last Updated**: April 30, 2026  
**Version**: 1.0 Production Ready  

Print this card for quick reference! 🖨️
