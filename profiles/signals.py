from django.db.models.signals import post_save, post_delete
from django.db import models
from django.dispatch import receiver
from tools.models import Tool
from votes.models import Vote


@receiver(post_save, sender=Vote)
def update_total_votes(sender, instance, created, **kwargs):
    if created:
        profile = instance.tool.user.profile
        profile.total_votes = Tool.objects.filter(
            user=instance.tool.user).aggregate(
                total_votes=models.Sum('votes')
                ).get('total_votes', 0)
        profile.save()


@receiver(post_delete, sender=Vote)
def decrease_total_votes(sender, instance, **kwargs):
    profile = instance.tool.user.profile
    profile.total_votes = Tool.objects.filter(
        user=instance.tool.user).aggregate(
            total_votes=models.Sum('votes')
            ).get('total_votes', 0)
    profile.save()


@receiver(post_save, sender=Tool)
def update_tool_count(sender, instance, created, **kwargs):
    if created:
        profile = instance.user.profile
        profile.tool_count = Tool.objects.filter(
            user=instance.user).count()
        profile.save()


@receiver(post_delete, sender=Tool)
def decrease_tool_count(sender, instance, **kwargs):
    profile = instance.user.profile
    profile.tool_count = Tool.objects.filter(
        user=instance.user).count()
    profile.save()
