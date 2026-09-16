from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q, Avg, F, ExpressionWrapper, DurationField
from django.http import JsonResponse
from problems.models import Problem, CATEGORY_CHOICES, STATUS_CHOICES
from problems.forms import ProblemForm, AdminProblemEditForm
from solutions.forms import SolutionForm
from ai_engine.services import analyze_problem
from ai_engine.models import DuplicateRecord
from datetime import datetime
from django.utils import timezone

@login_required
def problem_feed(request):
    problems = Problem.objects.exclude(status__in=['PENDING', 'REJECTED']).annotate(
        solution_count=Count('solutions', filter=Q(solutions__approval_status='APPROVED'))
    ).order_by('-created_at')
    category_filter = request.GET.get('category')
    status_filter = request.GET.get('status')
    search_query = request.GET.get('q')

    if category_filter and category_filter != 'All':
        problems = problems.filter(category=category_filter)
    if status_filter and status_filter != 'All':
        problems = problems.filter(status=status_filter)
    if search_query:
        problems = problems.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

    paginator = Paginator(problems, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = [choice[0] for choice in CATEGORY_CHOICES]
    statuses = [choice[0] for choice in STATUS_CHOICES]

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'statuses': statuses,
        'current_category': category_filter or 'All',
        'current_status': status_filter or 'All',
        'search_query': search_query or '',
    }
    return render(request, 'problems/feed.html', context)

@login_required
def submit_problem(request):
    if request.method == 'POST':
        form = ProblemForm(request.POST, request.FILES)
        if form.is_valid():
            problem = form.save(commit=False)
            problem.submitted_by = request.user
            problem.status = 'PENDING'
            analysis = analyze_problem(problem.title, problem.description)
            problem.ai_predicted_category = analysis['category']
            problem.ai_predicted_priority = analysis['priority']
            if not problem.category or problem.category == 'Other':
                problem.category = analysis['category']
            problem.priority = analysis['priority']
            problem.save()
            DuplicateRecord.objects.bulk_create([
                DuplicateRecord(
                    problem=problem,
                    similar_problem=duplicate['problem'],
                    similarity_score=duplicate['score'],
                )
                for duplicate in analysis['duplicates']
            ])
            messages.success(request, 'Your problem has been submitted and is pending admin approval.')
            return redirect('my_submissions')
    else:
        form = ProblemForm()
    return render(request, 'problems/submit.html', {'form': form})

@login_required
def problem_detail(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    is_admin = request.user.role == 'ADMIN'
    if not problem.is_public() and problem.submitted_by != request.user and not is_admin:
        messages.error(request, 'You do not have permission to view this problem.')
        return redirect('problem_feed')
    solutions = problem.solutions.filter(approval_status='APPROVED')
    if request.method == 'POST' and problem.is_public():
        sol_form = SolutionForm(request.POST)
        if sol_form.is_valid():
            sol = sol_form.save(commit=False)
            sol.problem = problem
            sol.submitted_by = request.user
            sol.save()
            messages.success(request, 'Your solution has been submitted and is pending admin approval.')
            return redirect('problem_detail', pk=pk)
    else:
        sol_form = SolutionForm() if problem.is_public() else None
    return render(request, 'problems/detail.html', {'problem': problem, 'solutions': solutions, 'sol_form': sol_form})

@login_required
def my_submissions(request):
    """Show a student's submissions with fresh, status-specific counts."""
    all_submissions = Problem.objects.filter(submitted_by=request.user)
    current_status = request.GET.get('status', 'All').upper()
    allowed_statuses = {'PENDING', 'APPROVED', 'REJECTED'}

    # Unknown/legacy filter values use the default tab instead of showing an
    # empty, misleading list.
    if current_status not in allowed_statuses:
        current_status = 'All'

    problems = all_submissions
    if current_status != 'All':
        problems = problems.filter(status=current_status)

    return render(request, 'problems/my_submissions.html', {
        'problems': problems.order_by('-created_at'),
        'current_status': current_status,
        **_submission_counts(all_submissions),
    })


def _submission_counts(submissions):
    """Calculate all dashboard badges in one database query."""
    return submissions.aggregate(
        total_count=Count('id'),
        pending_count=Count('id', filter=Q(status='PENDING')),
        approved_count=Count('id', filter=Q(status='APPROVED')),
        rejected_count=Count('id', filter=Q(status='REJECTED')),
    )


@login_required
def my_submission_counts(request):
    """Polling endpoint for live updates after a moderator changes a status."""
    submissions = Problem.objects.filter(submitted_by=request.user)
    return JsonResponse(_submission_counts(submissions))
