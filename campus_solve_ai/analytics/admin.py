from django.contrib import admin
from analytics.models import AdminAction
from ai_engine.models import DuplicateRecord

class AdminActionAdmin(admin.ModelAdmin):
    list_display = ('admin', 'action_type', 'problem', 'solution', 'timestamp')
    list_filter = ('action_type', 'timestamp')
    search_fields = ('admin__full_name', 'remarks')

admin.site.register(AdminAction, AdminActionAdmin)
admin.site.register(DuplicateRecord)
