from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


# Model for user profiles
class Profile(models.Model):
    """
    Represents a user profile.

    Args:
        models (django.db.models.Model):
            The base model class provided by Django.

    Returns:
        Profile: An instance of the Profile class.

    Attributes:
        user (django.contrib.auth.models.User):
            The user associated with the profile.
        created (datetime.datetime):
            The date and time when the profile was created.
        updated (datetime.datetime):
            The date and time when the profile was last updated.
        first_name (str):
            The first name of the user.
        last_name (str):
            The last name of the user.
        profile_description (str):
            A description of the user's profile.
        linkedin (str):
            The LinkedIn profile URL of the user.
        image (django.db.models.ImageField):
            An image associated with the user's profile.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    profile_description = models.TextField(max_length=500, blank=True)
    linkedin = models.URLField(max_length=200, blank=True)
    image = models.ImageField(default="../anonymdog_tnbngb",
                              upload_to="user-images/")
    tool_count = models.PositiveIntegerField(default=0)
    total_votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username

    # Signal receiver to create a profile for a new user
    def create_profile(sender, instance, created, **kwargs):
        """
        Create a profile for a newly created user.

        This function is a signal receiver that gets triggered
        when a new user is created.
        It creates a profile for the user by calling
        the `create` method of the `Profile` model.

        Args:
            sender (Type):
                The class of the sender.
            instance (object):
                The instance of the sender class that triggered the signal.
            created (bool):
                A boolean indicating whether the user was just created.

        Returns:
            None
        """
        if created:
            Profile.objects.create(user=instance)

    # Connect the signal receiver to the User model
    post_save.connect(create_profile, sender=User)


class BlacklistedToken(models.Model):
    token = models.TextField(max_length=500, unique=True)
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token
