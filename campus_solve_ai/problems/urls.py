from django.urls import path
from . import views

urlpatterns = [
    path('', views.problem_feed, name='problem_feed'),
    path('submit/', views.submit_problem, name='submit_problem'),
    path('<int:pk>/', views.problem_detail, name='problem_detail'),
    path('my-submissions/', views.my_submissions, name='my_submissions'),
]
