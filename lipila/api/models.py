"""
    This file contains the models for the student_transactions app.
"""
from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractUser

CITY_CHOICES = (
    ('KITWE', 'Kitwe'),
    ('LUSAKA', 'Lusaka'),
)

class MyUser(User):
    phone_number = models.CharField(max_length=20, blank=False, null=False)
    bio = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=10, default="Zambia")
    address = models.CharField(max_length=255, default="", blank=False, null=False)
    company = models.CharField(max_length=255, default="", blank=False, null=False)
    city = models.CharField(max_length=9, choices=CITY_CHOICES, default='KITWE')
    profile_image = models.ImageField(upload_to='img/profiles/', blank=True, null=True)


    REQUIRED_FIELDS = ['email', 'phone_number']

    @staticmethod
    def get_user_by_id(ids):
        return MyUser.objects.filter(id__in=str(ids))


class Product(models.Model):
    product_name = models.CharField(max_length=300)
    product_owner = models.ForeignKey(User, related_name='product',
                                      on_delete=models.CASCADE)
    price = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)


class LipilaDisbursement(models.Model):
    payer = models.ForeignKey(User,
                              related_name='disbursed',
                              on_delete=models.CASCADE,
                              )
    payee = models.ForeignKey(MyUser,
                              related_name='paid',
                              on_delete=models.CASCADE,
                              )
    payee_account = models.CharField(max_length=30)
    payment_amount = models.FloatField()
    payment_method = models.CharField(max_length=55)
    transaction_id = models.CharField(max_length=20)
    payment_date = models.DateField()
    description = models.CharField(max_length=255)

    def get_account_number(self):
        """ returns the username of the student"""
        return self.payee.phone_number

    def __str__(self):
        return "{} {} {} {} {} {} {}".format(self.payee,
                                             self.payment_amount,
                                             self.payment_method,
                                             self.transaction_id,
                                             self.payment_date,
                                             self.payee_account,
                                             self.description,
                                             )


class LipilaCollection(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    # currency = models.CharField(max_length=3)
    timestamp = models.DateTimeField(auto_now_add=True)
    reference_id = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    payer_account = models.CharField(max_length=10, null=False, blank=False)
    payer_name = models.CharField(max_length=100, null=True, blank=True)
    payer_email = models.EmailField(null=True, blank=True)
    payee = models.ForeignKey(User, related_name='payment',
                                      on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=(
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ))

    def get_reference_id(self):
        return self.reference_id