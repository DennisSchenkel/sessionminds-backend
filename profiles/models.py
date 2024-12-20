from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils.text import slugify


# Model for user profiles
class Profile(models.Model):
    """
    Represents a user profile.

    Args:
        models (django.db.models.Model):
            The base model class provided by Django.

    Methods:
        create_profile(sender, instance, created, **kwargs):
            Create a profile for a newly created user.
        save(*args, **kwargs):
            Generate a slug for the profile on save

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
        tool_count (int):
            The number of tools created by the user.
        total_votes (int):
            The total number of votes received by the user.
        slug (str):
            The slug field for the profile.

    Returns:
        Profile: An instance of the Profile class.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    profile_description = models.TextField(max_length=500, blank=True)
    linkedin = models.URLField(max_length=200, blank=True)
    twitter = models.URLField(max_length=200, blank=True)
    facebook = models.URLField(max_length=200, blank=True)
    instagram = models.URLField(max_length=200, blank=True)
    image = models.ImageField(
        default="../anonymdog_tnbngb", upload_to="user-images/"
        )
    tool_count = models.PositiveIntegerField(default=0)
    total_votes = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True, null=True, blank=True)

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

        Method:
            Profile.objects.create(user=instance):
                Create a profile for the newly created user

        Attributes:
            user (django.contrib.auth.models.User):
                The user associated with the profile.

        Returns:
            None
        """
        if created:
            Profile.objects.create(user=instance)

    # Generate a slug for the profile on save
    def save(self, *args, **kwargs):
        if self.first_name and self.last_name:
            new_slug = slugify(
                f"{self.first_name}-{self.last_name}-{self.user.id}"
                )
        else:
            new_slug = slugify(f"profile-{self.user.id}")

        # Check if the generated slug is unique
        # If not, append a number to make it unique
        unique_slug = new_slug
        num = 1
        while Profile.objects.filter(
            slug=unique_slug
        ).exclude(pk=self.pk).exists():
            unique_slug = f"{new_slug}-{num}"
            num += 1

        self.slug = unique_slug
        super().save(*args, **kwargs)

    # Connect the signal receiver to the User model
    post_save.connect(create_profile, sender=User)


# Model for storing blacklisted tokens
class BlacklistedToken(models.Model):
    """
    Represents a blacklisted token.

    Args:
        models (django.db.models.Model):
        The base model class provided by Django.

    Methods:
        __str__():
            Returns the token.

    Attributes:
        token (django.db.models.TextField):
            The token to be blacklisted.
        blacklisted_at (django.db.models.DateTimeField):
            The date and time when the token was blacklisted.

    Returns:
        BlacklistedToken: An instance of the BlacklistedToken class.
    """
    token = models.TextField(max_length=500, unique=True)
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token
