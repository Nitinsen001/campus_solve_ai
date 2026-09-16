import os
from django.core.wsgi import get_wsgi_application

settings_module = 'campus_solve_ai.settings.production' if os.getenv('VERCEL') else 'campus_solve_ai.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
application = get_wsgi_application()
