#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Ensure the media directory exists
mkdir -p media

# Copy media files from the existing directory
cp -r media/* media/

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate

# Load demo data
python manage.py loaddata demo_data.json

# Start the server
gunicorn yourproject.wsgi:application
