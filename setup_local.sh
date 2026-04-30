#!/bin/bash
# Local development setup script for CarrerPathPro
# Run this script to quickly set up the development environment

echo "=========================================="
echo "CarrerPathPro - Local Setup Script"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "ERROR: Python is not installed. Please install Python 3.9 or higher."
    exit 1
fi

echo "✓ Python found: $(python --version)"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Skipping..."
else
    python -m venv venv
    echo "✓ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip
echo "✓ Pip upgraded"
echo ""

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Create .env file if it doesn't exist
if [ -f ".env" ]; then
    echo ".env file already exists. Skipping..."
else
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "✓ .env file created"
    echo "  → Edit .env with your local settings if needed"
fi
echo ""

# Run migrations
echo "Running migrations..."
python manage.py migrate
echo "✓ Migrations completed"
echo ""

# Create superuser
read -p "Create a superuser account? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
    echo "✓ Superuser created"
else
    echo "Skipping superuser creation"
fi
echo ""

# Load sample data
read -p "Load sample assessment questions? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python manage.py seed_assessment_questions
    echo "✓ Assessment questions loaded"
else
    echo "Skipping sample data"
fi
echo ""

echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "To start the development server, run:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "Access the application at: http://127.0.0.1:8000/"
echo "Admin panel: http://127.0.0.1:8000/admin/"
echo ""
