# Campus Solve AI - Deployment Guide

## Deployment Files Created

1. **Procfile** - Defines how to run the application
2. **runtime.txt** - Specifies Python version
3. **production.py** - Production settings
4. **.env.example** - Environment variables template
5. **.gitignore** - Files to ignore in git

## Deployment Steps

### 1. Heroku Deployment

`ash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create new app
heroku create your-app-name

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key-here
heroku config:set DJANGO_SETTINGS_MODULE=campus_solve_ai.settings.production

# Add PostgreSQL database
heroku addons:create heroku-postgresql:mini

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser

# Collect static files
heroku run python manage.py collectstatic --noinput
``n
### 2. Railway Deployment

1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Railway will auto-deploy using Procfile

### 3. Render Deployment

1. Create new Web Service on Render
2. Connect your repository
3. Set build command: pip install -r requirements.txt
4. Set start command: gunicorn campus_solve_ai.wsgi
5. Add environment variables

### 4. DigitalOcean/VPS Deployment

`ash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3-pip python3-venv nginx -y

# Clone repository
git clone your-repo-url
cd campus_solve_ai

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Set environment variables
export DJANGO_SETTINGS_MODULE=campus_solve_ai.settings.production
export SECRET_KEY=your-secret-key

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser

# Run with Gunicorn
gunicorn campus_solve_ai.wsgi:application --bind 0.0.0.0:8000
``n
## Important Notes

1. **Change SECRET_KEY** in production
2. **Set DEBUG=False** in production
3. **Configure ALLOWED_HOSTS** with your domain
4. **Use PostgreSQL** for production (not SQLite)
5. **Set up SSL certificate** for HTTPS
6. **Configure email backend** for production
7. **Set up media file storage** (AWS S3, Cloudinary, etc.)

## Environment Variables Required

- SECRET_KEY - Django secret key
- DATABASE_URL - Database connection string
- DJANGO_SETTINGS_MODULE - Set to campus_solve_ai.settings.production
- ALLOWED_HOSTS - Your domain names
- DEBUG - Set to False

