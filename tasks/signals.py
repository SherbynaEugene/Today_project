from django.db.models.signals import post_save
from django.dispatch import receiver
from tasks.models import Task
from rating.services import reward_for_task_completion

@receiver(post_save, sender=Task)
def reward_after_task_completed(sender, instance, created, **kwargs):
    if instance.is_completed:
        reward_for_task_completion(instance)