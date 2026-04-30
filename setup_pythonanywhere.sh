#!/bin/bash
# PythonAnywhere Deployment Setup Script
# Run this script in PythonAnywhere Bash console to quickly set up the application

echo "=========================================="
echo "CarrerPathPro - PythonAnywhere Setup"
echo "=========================================="
echo ""

# Get username and domain
read -p "Enter your PythonAnywhere username: " USERNAME
read -p "Enter your project directory name: " PROJECT_DIR

# Navigate to home
cd ~

# Check if project exists
if [ ! -d "$PROJECT_DIR" ]; then
    echo "ERROR: Project directory not found at ~/$PROJECT_DIR"
    exit 1
fi

cd $PROJECT_DIR
echo "✓ In project directory: $(pwd)"
echo ""

# Create virtual environment
echo "Creating virtual environment (carrer)..."
mkvirtualenv --python=/usr/bin/python3.10 carrer
echo "✓ Virtual environment created"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Configure environment
echo "Setting up .env file..."
if [ -f ".env" ]; then
    echo "✓ .env file already exists"
else
    cp .env.example .env
    echo "✓ .env file created from template"
fi
echo ""

# Prompt for important environment variables
read -p "Enter Django SECRET_KEY (or leave blank to generate): " SECRET_KEY
if [ -z "$SECRET_KEY" ]; then
    SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
    echo "Generated SECRET_KEY: $SECRET_KEY"
fi

read -p "Enter database password for 'pathpro' user: " DB_PASSWORD

# Update .env file
echo "Updating .env file..."
# Note: This is a simple replacement, might need manual editing for complex cases
sed -i "s/your-super-secret-key-change-this-in-production/$SECRET_KEY/" .env
sed -i "s/your_password/$DB_PASSWORD/" .env
sed -i "s/yourusername/$USERNAME/" .env
sed -i "s/yourdomain.com/$USERNAME.pythonanywhere.com/" .env
sed -i "s/ENVIRONMENT=production/ENVIRONMENT=production/" .env
echo "✓ .env file updated"
echo ""

# Run migrations
echo "Running database migrations..."
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

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear
echo "✓ Static files collected"
echo ""

echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Go to Web tab in PythonAnywhere"
echo "2. Click your web app"
echo "3. Set WSGI configuration file to:"
echo "   /home/$USERNAME/$PROJECT_DIR/career_platform/wsgi.py"
echo ""
echo "4. Set Virtual environment to:"
echo "   /home/$USERNAME/.virtualenvs/carrer"
echo ""
echo "5. Add static file mapping:"
echo "   URL: /static/"
echo "   Directory: /home/$USERNAME/$PROJECT_DIR/staticfiles"
echo ""
echo "6. Click 'Reload' button to apply changes"
echo ""
echo "Check your domain: https://$USERNAME.pythonanywhere.com"
echo ""
