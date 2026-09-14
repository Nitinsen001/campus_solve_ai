from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('problems/', views.problem_moderation, name='problem_moderation'),
    path('problems/approve/<int:pk>/', views.approve_problem, name='approve_problem'),
    path('problems/reject/<int:pk>/', views.reject_problem, name='reject_problem'),
    path('problems/unapprove/<int:pk>/', views.unapprove_problem, name='unapprove_problem'),
    path('problems/delete/<int:pk>/', views.delete_problem, name='delete_problem'),
    path('problems/edit/<int:pk>/', views.edit_problem, name='edit_problem'),
    path('solutions/', views.solution_moderation, name='solution_moderation'),
    path('solutions/approve/<int:pk>/', views.approve_solution, name='approve_solution'),
    path('solutions/reject/<int:pk>/', views.reject_solution, name='reject_solution'),
    path('solutions/unapprove/<int:pk>/', views.unapprove_solution, name='unapprove_solution'),
    path('solutions/delete/<int:pk>/', views.delete_solution, name='delete_solution'),
    path('solutions/recommend/<int:pk>/', views.recommend_solution, name='recommend_solution'),
    path('solutions/unmark/<int:pk>/', views.unmark_solution, name='unmark_solution'),
]
