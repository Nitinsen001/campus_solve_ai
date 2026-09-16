import os
from django.core.asgi import get_asgi_application

settings_module = 'campus_solve_ai.settings.production' if os.getenv('VERCEL') else 'campus_solve_ai.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
application = get_asgi_application()
