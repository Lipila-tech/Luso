from django.db import models
from django.contrib.auth.models import User
from accounts.models import CreatorProfile, PatronProfile
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
        return f"{self.name} -> {self.price}"


class TierSubscriptions(models.Model):
    patron = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE, related_name='subscriptions')

    def __str__(self):
        return f"{self.patron}"


class Payments(models.Model):
    subscription = models.ForeignKey(TierSubscriptions, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subscription}"


class Contributions(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contributions_received')
    patron = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contributions_sent')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField()
    phone_number = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount}"
    

class Withdrawal(models.Model):
    creator = models.ForeignKey(CreatorProfile, on_delete=models.CASCADE, related_name='withdrawals')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    withdrawal_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Withdrawal - {self.creator.user.username} - Amount: {self.amount}"


class WithdrawalRequest(models.Model):
    creator = models.ForeignKey(CreatorProfile, on_delete=models.CASCADE, related_name='withdrawal_requests')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    processed_date = models.DateTimeField(blank=True, null=True)  # Optional for tracking processing time

    def __str__(self):
        return f"Withdrawal Request - {self.creator.user.username} - Amount: {self.amount}"
