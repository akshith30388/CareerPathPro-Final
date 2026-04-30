@echo off
REM Local development setup script for CarrerPathPro (Windows)
REM Run this script to quickly set up the development environment

echo.
echo ==========================================
echo CarrerPathPro - Local Setup Script (Windows)
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed. Please install Python 3.9 or higher.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [OK] Python found: %PYTHON_VERSION%
echo.

REM Create virtual environment
if exist "venv" (
    echo Virtual environment already exists. Skipping...
) else (
    echo Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo [OK] Pip upgraded
echo.

REM Install dependencies
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed
echo.

REM Create .env file if it doesn't exist
if exist ".env" (
    echo .env file already exists. Skipping...
) else (
    echo Creating .env file from .env.example...
    copy .env.example .env
    echo [OK] .env file created
    echo      ^> Edit .env with your local settings if needed
)
echo.

REM Run migrations
echo Running migrations...
python manage.py migrate
echo [OK] Migrations completed
echo.

REM Create superuser
set /p CREATE_SUPERUSER="Create a superuser account? (y/n): "
if /i "%CREATE_SUPERUSER%"=="y" (
    python manage.py createsuperuser
    echo [OK] Superuser created
) else (
    echo Skipping superuser creation
)
echo.

REM Load sample data
set /p LOAD_SAMPLE="Load sample assessment questions? (y/n): "
if /i "%LOAD_SAMPLE%"=="y" (
    python manage.py seed_assessment_questions
    echo [OK] Assessment questions loaded
) else (
    echo Skipping sample data
)
echo.

echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo To start the development server, run:
echo   venv\Scripts\activate.bat
echo   python manage.py runserver
echo.
echo Access the application at: http://127.0.0.1:8000/
echo Admin panel: http://127.0.0.1:8000/admin/
echo.
pause
