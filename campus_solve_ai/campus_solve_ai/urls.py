from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='login', permanent=False)),
    path('accounts/', include('accounts.urls')),
    path('problems/', include('problems.urls')),
    path('solutions/', include('solutions.urls')),
    path('analytics/', include('analytics.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('ai/', include('ai_engine.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
