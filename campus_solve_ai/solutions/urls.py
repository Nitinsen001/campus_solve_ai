from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='problem_feed', permanent=False)),
    path('submit/<int:problem_id>/', views.submit_solution, name='submit_solution'),
]
