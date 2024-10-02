#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Move the media folder from static files to the project level
mkdir -p "media"
mv "static/demo_media/"* "media"
echo "Media folder successfully moved to the project level."

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate

# Load demo data
python manage.py loaddata demo_data.json
