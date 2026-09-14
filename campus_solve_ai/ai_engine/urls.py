from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='problem_feed', permanent=False)),
    path('analyze/', views.analyze_text, name='analyze_text'),
]
