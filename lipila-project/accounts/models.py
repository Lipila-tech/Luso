from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


CREATOR_CATEGORY_CHOICES = (
    ('artist', 'Artist'),
    ('musician', 'Musician'),
    ('videocreator', 'Video Creator'),
    ('podcaster', 'Podcaster'),
    ('other', 'Other'),
)

CITY_CHOICES = (
    ('kitwe', 'Kitwe'),
    ('lusaka', 'Lusaka'),
    ('ndola', 'Ndola'),
)
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#     first_name = models.CharField(max_length=100, blank=True)
#     last_name = models.CharField(max_length=100, blank=True)
#     email = models.EmailField(max_length=150)
#     signup_confirmation = models.BooleanField(default=False)

#     def __str__(self):
#         return self.user.username

# @receiver(post_save, sender=User)
# def update_profile_signal(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()

class PatronProfile(models.Model):
    user = models.OneToOneField(  # Relate to the User model
        'auth.User',
        on_delete=models.CASCADE,
        primary_key=True,
    )
    profile_image = models.ImageField(upload_to='img/creators/', blank=True, null=True)
    account_number = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True)  # Increased length for wider range of cities
    

class CreatorProfile(models.Model):
    user = models.OneToOneField(  # Relate to the User model
        'auth.User',
        on_delete=models.CASCADE,
        primary_key=True,
    )
    profile_image = models.ImageField(upload_to='img/creators/', blank=True, null=True)
    account_number = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True)
    city = models.CharField(max_length=50, blank=True)  # Increased length for wider range of cities

    # You might want to consider using a ForeignKey to a separate Category model
    creator_category = models.CharField(max_length=50, blank=True)

    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)