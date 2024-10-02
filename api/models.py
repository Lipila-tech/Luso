from django.db import models
from django.conf import settings

TRANSACTION_STATUS = (
    ('pending', 'Pending'),
    ('completed', 'Completed'),
    ('failed', 'Failed'),
)


class AirtelTransaction(models.Model):
    reference = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100, unique=True)
    msisdn = models.CharField(max_length=15)  # Subscriber's phone number
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=10, choices=TRANSACTION_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.status}"


class LipilaDisbursement(models.Model):
    """Stores disbursement data"""
    api_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 related_name='disbursements',
                                 on_delete=models.CASCADE,
                                 null=True, blank=True)
    send_money_to = models.CharField(max_length=30)
    amount = models.FloatField()
    wallet_type = models.CharField(max_length=55)
    transaction_id = models.CharField(
        max_length=120, unique=True, blank=False, null=False)
    processed_date = models.DateField(auto_now_add=True)
    updated_at = models.DateField(null=True, blank=True)
    reference = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=TRANSACTION_STATUS, default='pending')

    class Meta:
        ordering = ['-updated_at']

    def get_transaction_id(self):
        return self.transaction_id

    def __str__(self):
        return f"Paid - {self.send_money_to} Amount - {self.amount} Status - {self.status}"


class LipilaCollection(models.Model):
    """
    Stores collection data.
    """
    api_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='payments_received',
                                 on_delete=models.CASCADE, null=True, blank=True)
    msisdn = models.CharField(max_length=30)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False, null=False)
    wallet_type = models.CharField(max_length=55)
    transaction_id = models.CharField(
        max_length=120, unique=True, blank=False, null=False)
    processed_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(null=True, blank=True)
    reference = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=TRANSACTION_STATUS, default='pending')

    def __str__(self):
        return f"Payer {self.msisdn} Amount - {self.amount} Status {self.status}"

    class Meta:
        ordering = ['-updated_at']

    def get_transaction_id(self):
        return self.transaction_id
