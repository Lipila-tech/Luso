from django.db import models
from django.contrib.auth.models import User
from accounts.models import CreatorProfile
from api.utils import generate_reference_id
# Options
STATUS_CHOICES = (
    ('pending', 'pending'),
    ('success', 'success'),
    ('failed', 'failed'),
    ('rejected', 'rejected'),
)

CREATOR_CATEGORY_CHOICES = (
    ('', ''),
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
ISP_CHOICES = (
    ('', ''),
    ('mtn', 'mtn'),
    ('airtel', 'airtel'),
)

INVOICE_STATUS_CHOICES = (
    ('pending', 'pending'),
    ('paid', 'paid'),
    ('rejected', 'rejected'),
)

ONETIME_AMOUNT = 100
FAN_AMOUNT = 25
SUPERFAN_AMOUNT = 50


class Tier(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    creator = models.ForeignKey(
        CreatorProfile, on_delete=models.CASCADE, related_name='tiers')
    updated_at = models.DateTimeField(auto_now=True)
    visible_to_fans = models.BooleanField(default=True)

    @classmethod
    def create_default_tiers(cls, creator):
        # Create default tiers if they don't exist
        defaults = [
            {"name": "Onetime", "price": ONETIME_AMOUNT,
                "desc": "Make a one-time Contribution to support the creator's work.",
                'creator': creator, 'visible': True},
            {"name": "Fan", "price": FAN_AMOUNT,
                "desc": "Support the creator and get access to exclusive content.",
                'creator': creator, 'visible': True},
            {"name": "Superfan", "price": SUPERFAN_AMOUNT,
                "desc": "Enjoy additional perks and behind-the-scenes content.",
                'creator': creator, 'visible': True}
        ]
        for tier_data in defaults:
            Tier.objects.create(
                name=tier_data["name"],
                description=tier_data["desc"],
                price=tier_data['price'],
                creator=tier_data['creator'],
                visible_to_fans=tier_data['visible']
                )

    def __str__(self):
        return f"Subscription: {self.name} -> Creator: {self.creator}"


class TierSubscriptions(models.Model):
    patron = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subscriptions')
    tier = models.ForeignKey(
        Tier, on_delete=models.CASCADE, related_name='subscriptions')

    def __str__(self):
        return f"{self.tier}"


class Transfer(models.Model):
    payer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tranfers')
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False)
    payer_account_number = models.CharField(max_length=300, null=True, blank=False)
    payee_account_number = models.CharField(max_length=300, null=True, blank=False)
    reference_id = models.CharField(max_length=40, unique=True, blank=False, null=False)
    network_operator = models.CharField(max_length=20, choices=ISP_CHOICES, default='')
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')


class SubscriptionPayments(models.Model):
    payee = models.ForeignKey(
        TierSubscriptions, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payer_account_number = models.CharField(max_length=300, null=True, blank=True)
    reference_id = models.CharField(max_length=40, unique=True, blank=False, null=False)
    network_operator = models.CharField(max_length=20, choices=ISP_CHOICES , default='mtn')
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.subscription}"


class Contributions(models.Model):
    payee = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='contributions_received')
    payer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='contributions_sent')
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=False)
    payer_account_number = models.CharField(max_length=300, null=True, blank=False)
    reference_id = models.CharField(max_length=40, unique=True, blank=False, null=False)
    network_operator = models.CharField(max_length=20, choices=ISP_CHOICES, default='')
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.amount}"


class WithdrawalRequest(models.Model):
    processed_date = models.DateTimeField(blank=True, null=True)
    creator = models.ForeignKey(
        CreatorProfile, on_delete=models.CASCADE, related_name='withdrawal_requests')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account_number = models.CharField(max_length=30)
    # reference_id = models.CharField(max_length=120, unique=True, blank=False, null=False)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES , default='pending')
    network_operator = models.CharField(max_length=20, choices=ISP_CHOICES , default='')
    reason = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        processed = True if self.processed_date else False
        return f"By - {self.creator.user.username} - Amount: {self.amount} - Processed - {self.processed_date}"


class ProcessedWithdrawals(models.Model):
    approved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_withdrawals')
    approved_date = models.DateTimeField(auto_now_add=True)
    rejected_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='rejected_withdrawals')
    rejected_date = models.DateTimeField(auto_now_add=True)
    # reference_id = models.CharField(max_length=120, unique=True, blank=False, null=False)
    withdrawal_request = models.ForeignKey(
        WithdrawalRequest, on_delete=models.CASCADE, related_name='withdrawals')
    status = models.CharField(max_length=20,choices=STATUS_CHOICES, default='pending')
    network_operator = models.CharField(max_length=20, choices=ISP_CHOICES , default='mtn')
    reason = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        if self.approved_by:
            return f"Withdrawal - {self.approved_by.username} - Status: {self.status}"
        else:
            return f"Withdrawal - Not Approved Yet - Status: {self.status}"