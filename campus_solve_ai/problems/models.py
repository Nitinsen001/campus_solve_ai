from django.db import models
from accounts.models import User

CATEGORY_CHOICES = (
    ('Water', 'Water'),
    ('Electricity', 'Electricity'),
    ('Internet/WiFi', 'Internet/WiFi'),
    ('Infrastructure', 'Infrastructure'),
    ('Classroom', 'Classroom'),
    ('Laboratory', 'Laboratory'),
    ('Hostel', 'Hostel'),
    ('Canteen', 'Canteen'),
    ('Transport', 'Transport'),
    ('Cleanliness', 'Cleanliness'),
    ('Safety', 'Safety'),
    ('Other', 'Other'),
)

PRIORITY_CHOICES = (
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
    ('Critical', 'Critical'),
)

STATUS_CHOICES = (
    ('PENDING', 'Pending Admin Approval'),
    ('APPROVED', 'Approved / Public'),
    ('Open', 'Open'),
    ('Under Review', 'Under Review'),
    ('Solution Available', 'Solution Available'),
    ('Resolved', 'Resolved'),
    ('Closed', 'Closed'),
    ('REJECTED', 'Rejected'),
)

class Problem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    ai_predicted_category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, null=True, blank=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Medium')
    ai_predicted_priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='PENDING')
    image = models.ImageField(upload_to='problem_images/', null=True, blank=True)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='problems')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_problems')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_duplicate = models.BooleanField(default=False)
    duplicate_of = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='duplicates')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def is_public(self):
        return self.status not in ['PENDING', 'REJECTED']

    def approved_solution_count(self):
        return self.solutions.filter(approval_status='APPROVED').count()

    def recommended_solution(self):
        return self.solutions.filter(approval_status='APPROVED', is_recommended=True).first()
