from django.db import models
from accounts.models import User
from problems.models import Problem
from solutions.models import Solution

ACTION_CHOICES = (
    ('APPROVE_PROBLEM', 'Approve Problem'),
    ('REJECT_PROBLEM', 'Reject Problem'),
    ('EDIT_PROBLEM', 'Edit Problem'),
    ('MERGE_PROBLEM', 'Merge Problem'),
    ('APPROVE_SOLUTION', 'Approve Solution'),
    ('REJECT_SOLUTION', 'Reject Solution'),
    ('MARK_RECOMMENDED', 'Mark Recommended'),
    ('ARCHIVE_SOLUTION', 'Archive Solution'),
)

class AdminAction(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_actions')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, null=True, blank=True)
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE, null=True, blank=True)
    action_type = models.CharField(max_length=50, choices=ACTION_CHOICES)
    remarks = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        target = self.problem or self.solution
        return f"{self.action_type} by {self.admin.full_name} on {target}"
