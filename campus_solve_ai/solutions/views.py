from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q
from problems.models import Problem
from solutions.models import Solution
from solutions.forms import SolutionForm

@login_required
def submit_solution(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    if not problem.is_public():
        messages.error(request, 'Solutions can only be submitted to approved public problems.')
        return redirect('problem_detail', pk=problem_id)
    if request.method == 'POST':
        form = SolutionForm(request.POST)
        if form.is_valid():
            sol = form.save(commit=False)
            sol.problem = problem
            sol.submitted_by = request.user
            sol.approval_status = 'PENDING'
            sol.save()
            messages.success(request, 'Your solution has been submitted and is pending admin approval.')
            return redirect('problem_detail', pk=problem_id)
    else:
        form = SolutionForm()
    return render(request, 'solutions/submit.html', {'form': form, 'problem': problem})
def my_submissions(request):
    problems = Problem.objects.filter(author=request.user)  # ya jaisa bhi filter hai
    context = {
        'problems': problems,
        'pending_count': problems.filter(status='PENDING').count(),
        'approved_count': problems.filter(status='APPROVED').count(),
        'rejected_count': problems.filter(status='REJECTED').count(),
        'current_status': request.GET.get('status', 'All'),
    }
    return render(request, 'my_submissions.html', context)