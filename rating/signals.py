
def some_signal_handler(sender, instance, **kwargs):
    from .services import reward_for_task_completion
    reward_for_task_completion(instance)