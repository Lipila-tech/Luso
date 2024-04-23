from django.db import models
from django.contrib.auth.models import User
from creators.models import CreatorUser


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
SUBSCRIPTION_CHOICES = (
    ('one', 'K 10'),
    ('two', 'K 20'),
    ('three', 'K 30'),
)


class LipilaUser(User):
    phone_number = models.CharField(
        max_length=20, blank=True, null=True)
    country = models.CharField(max_length=10, default="Zambia")
    address = models.CharField(
        max_length=255, default="", blank=True, null=True)
    company = models.CharField(
        max_length=255, default="", blank=True, null=True)
    city = models.CharField(
        max_length=9, choices=CITY_CHOICES, default='Kitwe')
    category = models.CharField(max_length=9, default='Member')
    profile_image = models.ImageField(
        upload_to='img/profiles/', blank=True, null=True)
    REQUIRED_FIELDS = ['phone_number']

    @staticmethod
    def get_user_by_id(ids):
        return LipilaUser.objects.filter(id__in=str(ids))

    def get_creators(self):
        """
        Returns a queryset of CreatorUser instances that the LipilaUser (patron) is following/joined.

        This method leverages the Patron model to efficiently retrieve creators associated with the patron.
        """

        if hasattr(self, 'patron'):  # Check if the LipilaUser has a Patron instance
            creator_ids = self.patron.creatoruser_set.values_list(
                'id', flat=True)
            return CreatorUser.objects.filter(pk=creator_ids)
        else:
            return CreatorUser.objects.none()  # Return an empty queryset if no Patron exists

        def __str__(self):
            return self.username


class Patron(models.Model):
    user = models.OneToOneField(
        LipilaUser, on_delete=models.CASCADE, primary_key=True)
    creators = models.ManyToManyField(CreatorUser)
    subscription = models.CharField(
        max_length=55, null=False, blank=False,
        choices=SUBSCRIPTION_CHOICES, default='one')
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user}"


class LipilaUserEmail(models.Model):
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


class LipilaHome(models.Model):
    hero_image = models.ImageField(
        upload_to='img/profiles/', blank=True, null=True)
    message = models.TextField()
    slogan = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = 'timestamp'


class Testimonial(models.Model):
    user = models.ForeignKey(
        LipilaUser, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = 'timestamp'
