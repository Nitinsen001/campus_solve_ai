from django.db import models
from problems.models import Problem

class DuplicateRecord(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='duplicate_records')
    similar_problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='similar_to_records')
    similarity_score = models.FloatField()
    admin_decision = models.CharField(max_length=50, choices=(
        ('PENDING', 'Pending'),
        ('DUPLICATE', 'Duplicate'),
        ('MERGE', 'Merge'),
        ('SEPARATE', 'Keep Separate'),
    ), default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Duplicate: {self.problem.title} ~ {self.similar_problem.title} ({self.similarity_score:.2f})"
