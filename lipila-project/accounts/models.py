from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# custom models
from .globals import default_socials, CITY_CHOICES, CREATOR_CATEGORY_CHOICES


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


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