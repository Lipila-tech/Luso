from django.db import models
from django.contrib.auth.models import User

# Options
STATUS_CHOICES = (
    ('pending', 'pending'),
    ('success', 'success'),
    ('failed', 'failed'),
)

USER_CATEGORY_CHOICES = (
    ('tick', 'Entrepreneur'),
    ('creator', 'Creator'),
    ('patron', 'Patron'),
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

class LipilaUser(User):
    phone_number = models.CharField(
        max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=10, default="Zambia")
    address = models.CharField(
        max_length=255, default="", blank=True, null=True)
    company = models.CharField(
        max_length=255, default="", blank=True, null=True)
    city = models.CharField(
        max_length=9, choices=CITY_CHOICES, default='KItwe')
    profile_image = models.ImageField(
        upload_to='img/profiles/', blank=True, null=True)
    user_category = models.CharField(
        max_length=30, choices=USER_CATEGORY_CHOICES, default='other')
    facebook_url = models.CharField(max_length=250, null=True, blank=True, default='')
    linkedin_url = models.CharField(max_length=250, null=True, blank=True, default='')
    twitter_url = models.CharField(max_length=250, null=True, blank=True, default='')
    instagram_url = models.CharField(max_length=250, null=True, blank=True, default='')

    REQUIRED_FIELDS = ['email']

    @staticmethod
    def get_user_by_id(ids):
        return LipilaUser.objects.filter(id__in=str(ids))

    def __str__(self):
        return self.username
    
# Create your models here.
class ContactInfo(models.Model):
    street = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    days = models.CharField(max_length=200)
    phone1 = models.CharField(max_length=200)
    phone2 = models.CharField(max_length=200)
    email1 = models.CharField(max_length=200)
    email2 = models.CharField(max_length=200)
    hours = models.CharField(max_length=200)
   
