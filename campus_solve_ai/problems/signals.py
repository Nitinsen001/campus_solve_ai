from django.db.models.signals import post_save
from django.dispatch import receiver
from problems.models import Problem

@receiver(post_save, sender=Problem)
def log_problem_action(sender, instance, created, **kwargs):
    if created:
        pass
