from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Count, Q
from problems.models import Problem
from problems.forms import AdminProblemEditForm
from solutions.models import Solution
from solutions.forms import SolutionForm
from ai_engine.services import analyze_problem
from ai_engine.models import DuplicateRecord

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'ADMIN':
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('problem_feed')
        return view_func(request, *args, **kwargs)
    return wrapper

@admin_required
def admin_dashboard(request):
    total_users = Problem.objects.filter(submitted_by__role='STUDENT').values('submitted_by').distinct().count()
    total_problems = Problem.objects.count()
    pending_problems = Problem.objects.filter(status='PENDING').count()
    approved_problems = Problem.objects.filter(status='APPROVED').count()
    open_problems = Problem.objects.filter(status='Open').count()
    resolved_problems = Problem.objects.filter(status='Resolved').count()
    pending_solutions = Solution.objects.filter(approval_status='PENDING').count()
    approved_solutions = Solution.objects.filter(approval_status='APPROVED').count()

    recent_problems = Problem.objects.order_by('-created_at')[:10]
    pending_solution_list = Solution.objects.filter(approval_status='PENDING').select_related('problem', 'submitted_by').order_by('-created_at')[:10]

    context = {
        'total_users': total_users,
        'total_problems': total_problems,
        'pending_problems': pending_problems,
        'approved_problems': approved_problems,
        'open_problems': open_problems,
        'resolved_problems': resolved_problems,
        'pending_solutions': pending_solutions,
        'approved_solutions': approved_solutions,
        'recent_problems': recent_problems,
        'pending_solution_list': pending_solution_list,
    }
    return render(request, 'dashboard/index.html', context)

@admin_required
def problem_moderation(request):
    problems = Problem.objects.order_by('-created_at')
    return render(request, 'dashboard/problem_moderation.html', {'problems': problems})

@admin_required
def solution_moderation(request):
    pending = Solution.objects.filter(approval_status='PENDING').select_related('problem', 'submitted_by').order_by('-created_at')
    approved = Solution.objects.filter(approval_status='APPROVED').select_related('problem', 'submitted_by').order_by('-created_at')[:20]
    rejected = Solution.objects.filter(approval_status='REJECTED').select_related('problem', 'submitted_by').order_by('-created_at')[:20]
    return render(request, 'dashboard/solution_moderation.html', {'pending': pending, 'approved': approved, 'rejected': rejected})

@admin_required
@require_POST
def approve_problem(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    problem.status = 'APPROVED'
    problem.approved_by = request.user
    problem.save()
    messages.success(request, f'Problem "{problem.title}" has been approved.')
    return redirect('problem_moderation')

@admin_required
@require_POST
def reject_problem(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    problem.status = 'REJECTED'
    problem.approved_by = request.user
    problem.save()
    messages.warning(request, f'Problem "{problem.title}" has been rejected.')
    return redirect('problem_moderation')

@admin_required
@require_POST
def unapprove_problem(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    problem.status = 'REJECTED'
    problem.approved_by = request.user
    problem.save(update_fields=['status', 'approved_by', 'updated_at'])
    messages.warning(request, f'Problem "{problem.title}" is no longer approved.')
    return redirect('admin_dashboard')

@admin_required
@require_POST
def delete_problem(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    title = problem.title
    problem.delete()
    messages.success(request, f'Problem "{title}" was deleted.')
    return redirect('admin_dashboard')

@admin_required
def edit_problem(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    if request.method == 'POST':
        form = AdminProblemEditForm(request.POST, instance=problem)
        if form.is_valid():
            form.save()
            messages.success(request, 'Problem updated successfully.')
            return redirect('problem_moderation')
    else:
        form = AdminProblemEditForm(instance=problem)
    return render(request, 'dashboard/edit_problem.html', {'form': form, 'problem': problem})

@admin_required
@require_POST
def approve_solution(request, pk):
    solution = get_object_or_404(Solution, pk=pk)
    solution.approval_status = 'APPROVED'
    solution.approved_by = request.user
    solution.save()
    messages.success(request, 'Solution approved.')
    return redirect('solution_moderation')

@admin_required
@require_POST
def reject_solution(request, pk):
    solution = get_object_or_404(Solution, pk=pk)
    solution.approval_status = 'REJECTED'
    solution.approved_by = request.user
    solution.save()
    messages.warning(request, 'Solution rejected.')
    return redirect('solution_moderation')

@admin_required
@require_POST
def unapprove_solution(request, pk):
    solution = get_object_or_404(Solution, pk=pk)
    solution.approval_status = 'REJECTED'
    solution.is_recommended = False
    solution.approved_by = request.user
    solution.save(update_fields=['approval_status', 'is_recommended', 'approved_by', 'updated_at'])
    messages.warning(request, 'Solution is no longer approved.')
    return redirect('solution_moderation')

@admin_required
@require_POST
def delete_solution(request, pk):
    solution = get_object_or_404(Solution, pk=pk)
    solution.delete()
    messages.success(request, 'Solution was deleted.')
    return redirect('solution_moderation')

@admin_required
@require_POST
def recommend_solution(request, pk):
    solution = get_object_or_404(Solution, pk=pk)
    solution.is_recommended = True
    solution.save()
    messages.success(request, 'Solution marked as recommended.')
    return redirect('solution_moderation')

@admin_required
@require_POST
def unmark_solution(request, pk):
    solution = get_object_or_404(Solution, pk=pk)
    solution.is_recommended = False
    solution.save()
    messages.success(request, 'Recommendation removed.')
    return redirect('solution_moderation')
