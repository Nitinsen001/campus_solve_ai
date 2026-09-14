from django.db.models.signals import post_save
from django.dispatch import receiver
from solutions.models import Solution

@receiver(post_save, sender=Solution)
def log_solution_action(sender, instance, created, **kwargs):
    if created:
        pass
