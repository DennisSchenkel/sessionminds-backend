from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from tools.models import Tool
from votes.models import Vote


def update_profile_total_votes(profile):
    profile.total_votes = Vote.objects.filter(
        tool__user=profile.user
        ).count() or 0
    profile.save(update_fields=['total_votes'])


def update_profile_tool_count(profile):
    profile.tool_count = Tool.objects.filter(
        user=profile.user
        ).count() or 0
    profile.save(update_fields=['tool_count'])


@receiver(post_save, sender=Vote)
@receiver(post_delete, sender=Vote)
def update_total_votes(sender, instance, **kwargs):
    profile = instance.tool.user.profile
    update_profile_total_votes(profile)


@receiver(post_save, sender=Tool)
@receiver(post_delete, sender=Tool)
def update_tool_count(sender, instance, **kwargs):
    profile = instance.user.profile
    update_profile_tool_count(profile)
