from django.db import models
from django.contrib.auth.models import User
from business.models import LipilaUser


# Global variables
STATUS_CHOICES = (
    ('pending', 'pending'),
    ('success', 'success'),
    ('failed', 'failed'),
)


class LipilaDisbursement(models.Model):
    """Stores data about transfers to multiple"""
    payer = models.ForeignKey(User,
                              related_name='disbursed',
                              on_delete=models.CASCADE,
                              )
    payee = models.ForeignKey(LipilaUser,
                              related_name='paid',
                              on_delete=models.CASCADE,
                              )
    payee_account = models.CharField(max_length=30)
    payment_amount = models.FloatField()
    payment_method = models.CharField(max_length=55)
    transaction_id = models.CharField(max_length=20)
    payment_date = models.DateField()
    description = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')

    def get_account_number(self):
        """ returns the username of the student"""
        return self.payee.phone_number

    def __str__(self):
        return "{} {} {} {} {} {} {} {}".format(self.payee,
                                                self.payment_amount,
                                                self.payment_method,
                                                self.transaction_id,
                                                self.payment_date,
                                                self.payee_account,
                                                self.description,
                                                self.status,
                                                )


class LipilaCollection(models.Model):
    """
    Stores data about bill collection to registered users.
    """
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    reference_id = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    payer = models.ForeignKey(LipilaUser, related_name='receipts',
                              on_delete=models.CASCADE)
    payee = models.ForeignKey(User, related_name='payment',
                              on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    
    class Meta:
        ordering = ['-timestamp']

    def get_reference_id(self):
        return self.reference_id

