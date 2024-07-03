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

default_socials = {
    'fb': 'https://facebook.com',
    'x': 'https://twitter.com',
    'lk': 'https://linkedin.com',
    'ig': 'https://instagram.com',
}

class PatronProfile(models.Model):
    user = models.OneToOneField(  # Relate to the User model
        'auth.User',
        on_delete=models.CASCADE,
        primary_key=True,
    )
    profile_image = models.ImageField(upload_to='img/creators/', blank=True, null=True)
    account_number = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.user.username


class CreatorProfile(models.Model):
    user = models.OneToOneField(  # Relate to the User model
        'auth.User',
        on_delete=models.CASCADE,
        primary_key=True,
    )
    profile_image = models.ImageField(upload_to='img/creators/', blank=True, null=True)
    account_number = models.CharField(max_length=20, blank=True, null=True)
    patron_title = models.CharField(max_length=150, unique=True)
    about = models.TextField(blank=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, default='Zambia')
    address = models.CharField(max_length=300, blank=True, default='Zambia resident')
    creator_category = models.CharField(max_length=50, choices=CREATOR_CATEGORY_CHOICES, default='other')
    facebook_url = models.URLField(blank=True, null=True, default=default_socials['fb'])
    twitter_url = models.URLField(blank=True, null=True, default=default_socials['x'])
    instagram_url = models.URLField(blank=True, null=True, default=default_socials['ig'])
    linkedin_url = models.URLField(blank=True, null=True, default=default_socials['lk'])

    def __str__(self):
        return self.user.username