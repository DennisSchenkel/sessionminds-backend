from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from tools.models import Tool
from votes.models import Vote


# Signal receiver to update the total votes for a user profile
def update_profile_total_votes(profile):
    """
    Update the total votes for a user profile.

    Args:
        profile (Profile): The user profile to update.
    """
    profile.total_votes = Vote.objects.filter(
        tool__user=profile.user
        ).count() or 0
    profile.save(update_fields=['total_votes'])


# Signal receiver to update the tool count for a user profile
def update_profile_tool_count(profile):
    """
    Update the tool count for a user profile.

    Args:
        profile (Profile): The user profile to update.
    """
    profile.tool_count = Tool.objects.filter(
        user=profile.user
        ).count() or 0
    profile.save(update_fields=['tool_count'])


# Signal receivers to update the total votes and tool count for a user profile
@receiver(post_save, sender=Vote)
@receiver(post_delete, sender=Vote)
def update_total_votes(sender, instance, **kwargs):
    """
    Update the total votes for a user profile.

    Args:
        sender: The sender of the signal.
        instance: The instance of the sender.
        kwargs: Additional keyword arguments.
    """
    profile = instance.tool.user.profile
    update_profile_total_votes(profile)


# Signal receivers to update the total votes and tool count for a user profile
@receiver(post_save, sender=Tool)
@receiver(post_delete, sender=Tool)
def update_tool_count(sender, instance, **kwargs):
    """
    Update the tool count for a user profile.

    Args:
        sender: The sender of the signal.
        instance: The instance of the sender.
        kwargs: Additional keyword arguments.
    """
    profile = instance.user.profile
    update_profile_tool_count(profile)
