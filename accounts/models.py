from django.db import models
from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
import mimetypes
# custom models
from .globals import (
    default_socials, CREATOR_CATEGORY_CHOICES, zambia_provinces,
    WALLET_TYPES)


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


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', 
        blank=True, 
        null=True, 
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    bio = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class UserSocialAuth(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    provider = models.CharField(max_length=50)  # e.g., 'tiktok', 'google', 'facebook'
    access_token = models.CharField(max_length=500)
    refresh_token = models.CharField(max_length=500, blank=True, null=True)
    token_expiry = models.DateTimeField(blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True)
    open_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'provider')

    def __str__(self):
        return self.user.username


class CreatorProfile(models.Model):
    user = models.OneToOneField(  # Relate to to user model
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    patron_title = models.CharField(
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9\-]+$',
                message='Patron title must be alphanumeric or contain dashes(-) only.',
                code='invalid_patron_title'
            ),
        ]
    )
    is_verified = models.BooleanField(default=False)
    creator_id_file = models.FileField(
        upload_to='creator_ids/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(
            allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])],
        verbose_name=_('Creator ID')
    )
    profile_image = models.ImageField(
        upload_to='img/creators/', blank=True, null=True)
    
    about = models.TextField(max_length=150, blank=True, null=True)
    location = models.CharField(
        max_length=50, choices=zambia_provinces, default=zambia_provinces['01'])
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
        return self.patron_title

    @property
    def file_type(self):
        if self.creator_id_file:
            file_path = self.creator_id_file.path
            file_type, _ = mimetypes.guess_type(file_path)
            return file_type
        return None



class PayoutAccount(models.Model):
    user_id = models.ForeignKey(  # Relate to to user model
        CreatorProfile,
        on_delete=models.SET_NULL, null=True, blank=True, related_name='bank'
    )
    wallet_type = models.CharField(max_length=50, choices=WALLET_TYPES, blank=True, null=True)
    wallet_provider = models.CharField(max_length=50, blank=True, null=True)
    account_name = models.CharField(max_length=50, blank=True, null=True)
    account_number = models.CharField(max_length=20, blank=True, null=True)
    account_currency = models.CharField(max_length=50, blank=True, null=True, default="ZMW")

    def __str__(self):
        return f"{self.wallet_provider} - {self.account_number}"

    @classmethod
    def create_default_bankaccount(cls, creator):
        # Create default tiers if they don't exist
        defaults = [
            {"wallet_type": WALLET_TYPES[0][0],
                'user': creator}
        ]
        for data in defaults:
            PayoutAccount.objects.create(
                user_id=data["user"],
                wallet_type=data["wallet_type"],
            )
