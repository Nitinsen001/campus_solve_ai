import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campus_solve_ai.settings')

import django
django.setup()

from accounts.models import User

if not User.objects.filter(email='admin@campussolve.ai').exists():
    User.objects.create_superuser('admin@campussolve.ai', 'Admin User', 'admin123')
    print("Superuser created: admin@campussolve.ai / admin123")
else:
    print("Superuser already exists")
