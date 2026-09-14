from django.contrib import admin
from problems.models import Problem

class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'priority', 'status', 'submitted_by', 'approved_by', 'created_at')
    list_filter = ('status', 'category', 'priority', 'created_at')
    search_fields = ('title', 'description', 'location')
    readonly_fields = ('submitted_by', 'created_at', 'updated_at', 'ai_predicted_category', 'ai_predicted_priority')
    fieldsets = (
        ('Problem Details', {'fields': ('title', 'description', 'location', 'category', 'priority', 'status')}),
        ('AI Predictions', {'fields': ('ai_predicted_category', 'ai_predicted_priority')}),
        ('Submission Info', {'fields': ('submitted_by', 'approved_by', 'image', 'is_duplicate', 'duplicate_of')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )

admin.site.register(Problem, ProblemAdmin)
