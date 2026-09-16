from django.contrib import admin
from solutions.models import Solution

class SolutionAdmin(admin.ModelAdmin):
    list_display = ('problem', 'submitted_by', 'approval_status', 'is_recommended', 'approved_by', 'created_at')
    list_filter = ('approval_status', 'is_recommended', 'created_at')
    search_fields = ('solution_text', 'problem__title', 'submitted_by__full_name', 'submitted_by__email')
    readonly_fields = ('submitted_by', 'created_at', 'updated_at')

admin.site.register(Solution, SolutionAdmin)
