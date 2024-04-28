from django.db import models
from LipilaInfo.models import LipilaUser
from django.contrib.auth.models import AbstractBaseUser, Group, Permission, BaseUserManager

# Options
STATUS_CHOICES = (
    ('pending', 'pending'),
    ('success', 'success'),
    ('failed', 'failed'),
)

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

INVOICE_STATUS_CHOICES = (
    ('pending', 'pending'),
    ('paid', 'paid'),
    ('rejected', 'rejected'),
)

ONETIME_AMOUNT = 50
FAN_AMOUNT = 10
SUPERFAN_AMOUNT = 30


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    is_patron = models.BooleanField(default=False)
    is_creator = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        Group, verbose_name='groups', blank=True, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(
        Permission, verbose_name='user permissions', blank=True, related_name='custom_user_set')
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Patron(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    subscribed = models.ManyToManyField(
        'CreatorUser', related_name='subscribers')
    account_number = models.CharField(
        max_length=20, blank=True, null=True)
    city = models.CharField(
        max_length=9, choices=CITY_CHOICES, default='Kitwe')
    profile_image = models.ImageField(
        upload_to='img/profiles/', blank=True, null=True)


class CreatorUser(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(blank=True, null=True)
    account_number = models.CharField(
        max_length=20, blank=True, null=True)
    # subscribers = models.ManyToManyField(Patron, related_name='subscribed_creators')
    city = models.CharField(
        max_length=9, choices=CITY_CHOICES, default='Kitwe')
    profile_image = models.ImageField(
        upload_to='img/profiles/', blank=True, null=True)
    category = models.CharField(max_length=9, default='Creator')
    creator_category = models.CharField(
        max_length=30, choices=CREATOR_CATEGORY_CHOICES, default='other')
    facebook_url = models.CharField(
        max_length=250, null=True, blank=True, default='')
    linkedin_url = models.CharField(
        max_length=250, null=True, blank=True, default='')
    twitter_url = models.CharField(
        max_length=250, null=True, blank=True, default='')
    instagram_url = models.CharField(
        max_length=250, null=True, blank=True, default='')
    timestamp = models.DateTimeField(auto_now_add=True)


class Tier(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @classmethod
    def create_default_tiers(cls):
        # Create default tiers if they don't exist
        defaults = [
            {"name": "Onetime", "price": ONETIME_AMOUNT},
            {"name": "Fan", "price": FAN_AMOUNT},
            {"name": "Superfan", "price": SUPERFAN_AMOUNT}
        ]
        for tier_data in defaults:
            Tier.objects.get_or_create(
                name=tier_data["name"], defaults=tier_data)

    def __str__(self):
        return f"{self.name} -> {self.price}"


class Contribution(models.Model):
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='contributions_received')
    patron = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='contributions_made')
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contribution of {self.amount} by {self.patron} to {self.creator} on {self.contribution_date}"
