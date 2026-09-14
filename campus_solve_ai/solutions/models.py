from django.db import models
from problems.models import Problem
from accounts.models import User

APPROVAL_CHOICES = (
    ('PENDING', 'Pending'),
    ('APPROVED', 'Approved'),
    ('REJECTED', 'Rejected'),
    ('ARCHIVED', 'Archived'),
)

class Solution(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='solutions')
    solution_text = models.TextField()
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solutions')
    approval_status = models.CharField(max_length=20, choices=APPROVAL_CHOICES, default='PENDING')
    is_recommended = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_solutions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_recommended', '-created_at']

    def __str__(self):
        return f"Solution for {self.problem.title} by {self.submitted_by.full_name}"
