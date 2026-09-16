import os
from django.core.wsgi import get_wsgi_application

settings_module = 'campus_solve_ai.settings.production' if os.getenv('VERCEL') else 'campus_solve_ai.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
# Vercel's Python runtime discovers WSGI applications through a top-level
# variable named ``app``.  Keep ``application`` as an alias for Django and
# other WSGI hosts that use the conventional name.
app = get_wsgi_application()
application = app
