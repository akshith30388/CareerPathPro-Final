# CareerPath Pro

CareerPath Pro is a Django-based counseling platform with role-based dashboards for students, counselors, and admins.

## Core Features
- Authentication with role-based access (`student`, `counselor`, `admin`)
- Career assessment + recommendations
- Appointment booking and counselor management
- Chat between students and counselors
- Student assignment engine with auto-grading and topic analysis
- Real-time counselor updates (Django Channels + WebSocket)

## New Assignment Workflow
- `GET /student/assignments/` - list active assignments
- `GET /student/assignments/<id>/start/` - create/resume submission
- `GET|POST /student/assignments/<id>/take/` - answer questions and save progress
- `POST /student/assignments/<id>/submit/` - submit, auto-grade, generate topic analysis
- `GET /student/assignments/<id>/result/` - score card, grade, chart, topic strengths, answer review

## Real-Time Counselor Sync
- `POST /student/select-counselor/<counselor_id>/` assigns counselor to student
- Counselor socket endpoint: `/ws/counselor/<counselor_id>/`
- Student socket endpoint: `/ws/student/<student_id>/`
- Live events:
  - `student_assigned`
  - `assignment_submitted`
  - `student_profile_update`

## Settings Structure
The project now uses split settings under `config/settings/`:
- `config/settings/base.py`
- `config/settings/local.py` (DEBUG=True, SQLite)
- `config/settings/production.py` (DEBUG=False, MySQL, WhiteNoise, Redis channel layer)

`manage.py` selects settings by `ENVIRONMENT` (`local` or `production`).
`career_platform/wsgi.py` points to `config.settings.production` for PythonAnywhere deployment.

## Local Setup
1. Create env file:
```bash
copy .env.example .env
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```
4. Start server:
```bash
python manage.py runserver
```

## Production Notes (PythonAnywhere + MySQL)
1. Set `ENVIRONMENT=production` in `.env`
2. Fill all DB keys from `.env.example`:
   - `DATABASE_NAME`
   - `DATABASE_USER`
   - `DATABASE_PASSWORD`
   - `DATABASE_HOST`
   - `DATABASE_PORT`
3. Set:
   - `SECRET_KEY`
   - `ALLOWED_HOSTS=yourusername.pythonanywhere.com`
   - `REDIS_URL`
4. Run:
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

## Main App Routes
- `/users/`
- `/student/`
- `/counselor/`
- `/assessments/`
- `/appointments/`
- `/recommendations/`
- `/chat/`
- `/dashboard/`
- `/ws/status/` (HTTP health endpoint for websocket module)
