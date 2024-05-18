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
    ('patron', 'PatronProfile'),
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
   

class ContactInfo(models.Model):
    street = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    days = models.CharField(max_length=200)
    phone1 = models.CharField(max_length=200)
    phone2 = models.CharField(max_length=200)
    email1 = models.CharField(max_length=200)
    email2 = models.CharField(max_length=200)
    hours = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.street} {self.location} {self.phone1}"
    
    class Meta:
        get_latest_by = 'timestamp'


class HeroInfo(models.Model):
    hero_image = models.ImageField(
        upload_to='img/profiles/', blank=True, null=True)
    message = models.TextField()
    slogan = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Slogan: {self.message} msg: {self.message} date: {self.timestamp}"

    class Meta:
        get_latest_by = 'timestamp'


class AboutInfo(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = 'timestamp'

class UserTestimonial(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = 'timestamp'


class CustomerMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, default='', null=True, blank=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.email} {self.subject}"

    class Meta:
        get_latest_by = 'timestamp'