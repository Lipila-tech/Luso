from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# custom models
from .globals import (
    default_socials, CREATOR_CATEGORY_CHOICES, zambia_provinces)


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


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_creator = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    has_group = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Send an email to this user.
        """
        send_mail(subject, message, from_email or settings.DEFAULT_FROM_EMAIL, [
                  self.email], **kwargs)


class CreatorProfile(models.Model):
    user = models.OneToOneField(  # Relate to to user model
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    profile_image = models.ImageField(
        upload_to='img/creators/', blank=True, null=True)
    account_number = models.CharField(max_length=20, blank=True, null=True)
    patron_title = models.CharField(max_length=150, unique=True)
    about = models.TextField(max_length=300, blank=True, null=True)
    location = models.CharField(max_length=50, choices=zambia_provinces, default=zambia_provinces['01'])
    adults_group = models.BooleanField(default=False)
    country = models.CharField(max_length=50, blank=True, default='Zambia')
    address = models.CharField(
        max_length=300, blank=True, null=True)
    creator_category = models.CharField(
        max_length=50, choices=CREATOR_CATEGORY_CHOICES, default='')
    facebook_url = models.URLField(
        blank=True, null=True, default=default_socials['fb'])
    twitter_url = models.URLField(
        blank=True, null=True, default=default_socials['x'])
    instagram_url = models.URLField(
        blank=True, null=True, default=default_socials['ig'])
    linkedin_url = models.URLField(
        blank=True, null=True, default=default_socials['lk'])

    def __str__(self):
        return self.user.username
