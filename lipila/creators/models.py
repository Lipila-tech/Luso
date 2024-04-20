from django.db import models
from django.contrib.auth.models import User
from LipilaInfo.models import LipilaUser
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

SUBSCRIPTION_CHOICES = (
    ('one', 'K 10'),
    ('two', 'K 20'),
    ('three', 'K 30'),
)


class CreatorUser(User):
    phone_number = models.CharField(
        max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=10, default="Zambia")
    address = models.CharField(
        max_length=255, default="", blank=True, null=True)
    company = models.CharField(
        max_length=255, default="", blank=True, null=True)
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

    REQUIRED_FIELDS = ['email']

    @staticmethod
    def get_user_by_id(ids):
        return CreatorUser.objects.filter(id__in=str(ids))

    def __str__(self):
        return self.username


class Patron(models.Model):
    username = models.ForeignKey(LipilaUser, on_delete=models.CASCADE)
    creator = models.ForeignKey(CreatorUser, on_delete=models.CASCADE)
    subscription = models.CharField(
        max_length=55, null=False, blank=False,
        choices=SUBSCRIPTION_CHOICES, default='one')
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username}"
