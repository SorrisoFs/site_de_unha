#!/bin/bash
# Build script for Render

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Seed initial data
python manage.py seed_data

# Create superuser if not exists (optional)
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@nailsalon.com', 'admin123')
    print('Superuser admin criado!')
"
