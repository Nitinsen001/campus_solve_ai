from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Avg, F, ExpressionWrapper, DurationField
from django.db.models.functions import TruncMonth
from problems.models import Problem
from solutions.models import Solution
from accounts.models import User
from ai_engine.models import DuplicateRecord

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'ADMIN':
            from django.contrib import messages
            from django.shortcuts import redirect
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('problem_feed')
        return view_func(request, *args, **kwargs)
    return wrapper

@admin_required
def analytics_dashboard(request):
    total_problems = Problem.objects.count()
    total_users = User.objects.filter(role='STUDENT').count()
    pending_problems = Problem.objects.filter(status='PENDING').count()
    approved_problems = Problem.objects.filter(status='APPROVED').count()
    open_problems = Problem.objects.filter(status='Open').count()
    resolved_problems = Problem.objects.filter(status='Resolved').count()
    pending_solutions = Solution.objects.filter(approval_status='PENDING').count()
    approved_solutions = Solution.objects.filter(approval_status='APPROVED').count()

    category_data = Problem.objects.filter(status='APPROVED').values('category').annotate(count=Count('id')).order_by('-count')
    location_data = Problem.objects.filter(status='APPROVED').values('location').annotate(count=Count('id')).order_by('-count')[:10]
    status_data = Problem.objects.values('status').annotate(count=Count('id')).order_by('-count')
    monthly_data = Problem.objects.filter(status='APPROVED').annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).order_by('month')
    priority_data = Problem.objects.filter(status='APPROVED').values('priority').annotate(count=Count('id'))
    resolution_data = Problem.objects.filter(status__in=['Resolved', 'Closed']).annotate(
        resolution_time=ExpressionWrapper(F('updated_at') - F('created_at'), output_field=DurationField())
    )
    avg_resolution = resolution_data.aggregate(avg=Avg('resolution_time'))['avg']
    duplicate_count = DuplicateRecord.objects.filter(admin_decision='DUPLICATE').count()
    duplicate_rate = round((duplicate_count / total_problems * 100), 2) if total_problems else 0
    solution_per_problem = Problem.objects.filter(status='APPROVED').annotate(sol_count=Count('solutions', filter=Q(solutions__approval_status='APPROVED'))).aggregate(avg=Avg('sol_count'))['avg']
    resolution_success_rate = round((resolved_problems / approved_problems * 100), 2) if approved_problems else 0

    monthly_labels = []
    monthly_values = []
    for m in monthly_data:
        monthly_labels.append(m['month'].strftime('%Y-%m') if m['month'] else 'N/A')
        monthly_values.append(m['count'])

    context = {
        'total_problems': total_problems,
        'total_users': total_users,
        'pending_problems': pending_problems,
        'approved_problems': approved_problems,
        'open_problems': open_problems,
        'resolved_problems': resolved_problems,
        'pending_solutions': pending_solutions,
        'approved_solutions': approved_solutions,
        'category_data': list(category_data),
        'location_data': list(location_data),
        'status_data': list(status_data),
        'monthly_data': list(monthly_data),
        'priority_data': list(priority_data),
        'avg_resolution': avg_resolution,
        'duplicate_rate': duplicate_rate,
        'solution_per_problem': round(solution_per_problem, 2) if solution_per_problem else 0,
        'resolution_success_rate': resolution_success_rate,
        'monthly_labels': monthly_labels,
        'monthly_values': monthly_values,
    }
    return render(request, 'analytics/dashboard.html', context)
