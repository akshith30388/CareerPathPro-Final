# 🎓 Career Guidance & Counseling Platform

A full-stack Django web application that helps students discover career paths through AI-powered assessments, expert counseling sessions, and personalized recommendations.

---

## 🚀 Quick Start (Local)

### 0. Create .env
```bash
copy .env.example .env
```

Set these for local use:
```
ENVIRONMENT=local
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Seed Assessment Questions
```bash
python manage.py seed_assessment_questions
```

### 4. Create Superuser (optional — already seeded below)
```bash
python manage.py createsuperuser
```

### 5. Run Server
```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000/**

---

## 👤 Demo Accounts

| Role       | Username      | Password       | Dashboard URL                  |
|------------|---------------|----------------|-------------------------------|
| Admin      | `admin`       | `Admin@1234`   | http://127.0.0.1:8000/dashboard/admin/ |
| Student    | `student1`    | `Student@1234` | http://127.0.0.1:8000/dashboard/student/ |
| Counselor  | `counselor1`  | `Counsel@1234` | http://127.0.0.1:8000/dashboard/counselor/ |
| Django Admin | `admin`     | `Admin@1234`   | http://127.0.0.1:8000/admin/ |

---

## 📁 Project Structure

```
career_platform/          ← Django project settings & URLs
users/                    ← CustomUser, StudentProfile, CounselorProfile
assessments/              ← MCQ Questions, Assessment Results
appointments/             ← Appointment booking, Feedback
recommendations/          ← AI-based Career Recommendations + Engine
chat/                     ← Real-time AJAX chat system
dashboard/                ← Role dashboards, Resume Builder
templates/                ← All HTML templates (Bootstrap 5)
static/css/               ← Custom CSS styles
```

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔐 Authentication | Register, Login, Logout with role-based access |
| 📋 Career Assessment | 15 MCQ questions (Aptitude, Interest, Personality) |
| 🤖 AI Recommendations | Rule-based engine maps scores to career paths |
| 🗓️ Appointment Booking | Students book sessions, counselors confirm/reject |
| 💬 Chat System | AJAX-based real-time messaging with polling |
| 📄 Resume Builder | Dynamic form with Education & Experience sections |
| ⭐ Feedback System | Students rate completed counseling sessions |
| 📊 Admin Dashboard | Analytics: users, appointments, top careers |

---

## 🛠️ Tech Stack

- **Backend**: Python 3.12, Django 6.0
- **Frontend**: Bootstrap 5, Bootstrap Icons, Vanilla JavaScript
- **Database**: SQLite (local), MySQL (production)
- **Auth**: Django built-in auth with custom `AbstractUser`

---

## 🔗 Key URLs

| URL | Description |
|-----|-------------|
| `/` | Landing / Home page |
| `/users/register/` | Student & Counselor registration |
| `/users/login/` | Login page |
| `/dashboard/` | Auto-redirects by role |
| `/assessments/` | Assessment start page |
| `/assessments/take/` | Take the MCQ test |
| `/recommendations/` | Career recommendations list |
| `/appointments/book/` | Book a counseling session |
| `/appointments/my/` | Student's appointments |
| `/appointments/manage/` | Counselor's appointment management |
| `/chat/` | Messages inbox |
| `/dashboard/resume/builder/` | Resume builder |
| `/dashboard/resume/preview/` | Resume preview & print |
| `/admin/` | Django admin panel |

---

## ⚙️ Settings & Environments

This project uses split settings:

- `career_platform/settings/base.py`
- `career_platform/settings/local.py`
- `career_platform/settings/production.py`

The settings module is selected via `ENVIRONMENT` in `.env`.

---

## 🚀 PythonAnywhere Deployment (MySQL)

### 1. Create MySQL Database
Create a database named `pathpro` in PythonAnywhere.

### 2. Configure .env on PythonAnywhere
```env
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourusername.pythonanywhere.com
DATABASE_URL=mysql://pathpro:your_password@127.0.0.1:3306/pathpro
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Migrate + Static
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

### 5. Configure WSGI
In the PythonAnywhere Web tab:

- **WSGI file**: `/home/yourusername/CarrerPathPro/career_platform/wsgi.py`
- **Source code**: `/home/yourusername/CarrerPathPro`
- **Working dir**: `/home/yourusername/CarrerPathPro`

### 6. Static Files Mapping
Set static files:

- URL: `/static/`
- Directory: `/home/yourusername/CarrerPathPro/staticfiles`

### 7. Reload Web App
Click **Reload** in PythonAnywhere.

