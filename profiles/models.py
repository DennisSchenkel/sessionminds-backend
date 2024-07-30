from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    profile_description = models.TextField(max_length=500, blank=True)
    linkedin = models.URLField(max_length=200, blank=True)
    image = models.ImageField(default='../anonymdog_tnbngb',
                              upload_to='user-images/')

    def __str__(self):
        return f'{self.user} Profile'


def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


post_save.connect(create_profile, sender=User)
