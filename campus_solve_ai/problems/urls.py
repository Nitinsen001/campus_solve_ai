from django.urls import path
from . import views

urlpatterns = [
    path('', views.problem_feed, name='problem_feed'),
    path('submit/', views.submit_problem, name='submit_problem'),
    path('<int:pk>/vote/', views.vote_problem, name='vote_problem'),
    path('my-submissions/counts/', views.my_submission_counts, name='my_submission_counts'),
    path('<int:pk>/', views.problem_detail, name='problem_detail'),
    path('my-submissions/', views.my_submissions, name='my_submissions'),
]
